from __future__ import absolute_import, print_function

import base64
import logging
import os
from os import path

from git import Repo
import boto3
import yaml

from .configreader import ConfigYamlReader, ConfigException
from .runtimes import AVAILABLE_RUNTIMES


# Global INFO for all loggers, including boto
logging.basicConfig(level=os.environ.get('LOG_LEVEL', logging.INFO))
logger = logging.getLogger('LambdaManager')


def _get_git_release(repo_dir='.'):
    repo = Repo(repo_dir)
    hash_name = repo.head.commit.hexsha
    if len(repo.index.diff(None)) > 0:
        # Changes not stashed
        hash_name += 'm'
    try:
        if len(repo.index.diff(HEAD)) > 0:
            # Changes added to next commit
            hash_name += 'h'
    except:
        pass

    return hash_name


class S3FunctionUploader:

    def __init__(self, bucket_name):
        self.s3_client = boto3.client('s3')
        self.bucket = bucket_name

        if not any(
            item['Name'] == self.bucket
            for item in self.s3_client.list_buckets().get('Buckets', [])
        ):
            logger.debug('Creating bucket s3://{0}'.format(self.bucket))
            self.s3_client.create_bucket(
                ACL='private',
                Bucket=self.bucket
            )

    def upload(self, local_filename, s3_filename):
        """ Stream the zip called local_filename to s3://bucket/s3_filename """

        logger.debug('writting file {0} into {1}/'.format(
            local_filename,
            self.bucket,
            s3_filename)
        )

        self.s3_client.upload_file(
            local_filename,
            self.bucket,
            s3_filename)


class AwsLambdaManager:

    def __init__(self, config):
        """
            config = {
                'the_visible_lambda_function_name': {
                    'Runtime': 'python2.7',
                    'Role': 'a-iam-role',
                    'Handler': 'module_name.lambda_handler',
                    'Description': 'A function description',  # optional
                    'Code': {
                       'S3Bucket': 'the-bucket-name-to-upload-releases',
                       'S3KeyPath': 'route/to/releases/directory',
                       'Directory': 'path/to/code/directory',
                    },
                    'MemorySize': 128,
                    'Timeout': 120,  # optional
                    'VpcConfig': {  # optional
                        'SubnetIds': [
                            'string',
                        ],
                        'SecurityGroupIds': [
                            'string',
                        ],
                    },
                    'Environment': {  # optional
                        'Variables': {
                            'KEY1': 'VALUE1',
                            'KEY2': 'VALUE2',
                            'KEY3': 'VALUE3',
                        }
                    },
                }
            }
        """
        self.config = config
        self.aws_lambda = boto3.client('lambda')

        self.function_selected = None
        self.function_config = {}

    def available_functions(self):
        """
            Return a list of the function names available in the config file
        """
        return self.config.keys()

    def select_function(self, name=None):
        """
            Select a function from config file to operate over it
        """
        if not name and len(self.available_functions()) == 1:
            self.function_selected = self.available_functions()[0]
        elif name in self.available_functions():
            self.function_selected = name
        else:
            raise self.FunctionNotFoundError("The function {0} is not present "
                                             "in the config file".format(name))
        self.function_config = self.config[self.function_selected]
        self.runtime = AVAILABLE_RUNTIMES[self.function_config['Runtime']]

    def get_function_configuration(self):
        """
            Return a dict with the basic function properties valid for aws
        """
        # Set required properties
        function_definition = {
            key: self.function_config[key]
            for key in (
                'Runtime',
                'Role',
                'Handler',
                'MemorySize',
            )
        }

        # Set optional properties
        function_definition.update({
            key: self.function_config[key]
            for key in (
                'Environment',
                'Description',
                'Timeout',
                'VpcConfig',
            )
            if self.function_config.get(key)
        })

        function_definition['FunctionName'] = self.function_selected

        return function_definition

    def create_package(self, release_tag=''):
        """ Create a temporary zip package"""

        code_directory = self.function_config['Code']['Directory']
        package_name = self.function_selected
        hash_release = _get_git_release()
        logger.info("Creating package with git release {0}".format(hash_release))

        lp = self.runtime['packager'](
            package_name,
            hash_release + release_tag,
            code_directory,
            target_directory='.')

        lp.build_and_save()

        self.hash_release = hash_release
        self.local_filename = lp.filename

    def upload_package(self, filename=None):
        """ Upload the package to S3 """
        logger.info("Uploading the package to S3")
        s3f = S3FunctionUploader(self.function_config['Code']['S3Bucket'])
        self.s3_filename = path.join(
            self.function_config['Code']['S3KeyPath'],
            path.basename(filename or self.local_filename)
        )
        s3f.upload(filename or self.local_filename,
                   self.s3_filename)


    def create_function(self):
        """ Create a function in aws lambda """
        logger.info("Preparing stuf to create function")
        self.create_package('devel')

        self.upload_package()

        function_definition = self.get_function_configuration()

        # Set the first release Code block
        function_definition['Code'] = {
            'S3Bucket': self.function_config['Code']['S3Bucket'],
            'S3Key': self.s3_filename,
        }

        function_definition['Publish'] = True

        logger.info("Creating function")
        return self.aws_lambda.create_function(**function_definition)

    def function_exists(self):
        """
            Check if the function is already created in aws
        """
        try:
            self.aws_lambda.get_function(
                FunctionName=self.function_selected
            )
            return True
        except self.aws_lambda.exceptions.ResourceNotFoundException:
            return False

    def create_release(self, alias="devel"):
        """
            publish version in lambda with alias "tag"
        """
        self.create_package(alias)

        self.upload_package()

        logger.info("Creating release {0}".format(self.hash_release))

        response_code = self.aws_lambda.update_function_code(
            FunctionName=self.function_selected,
            S3Bucket=self.function_config['Code']['S3Bucket'],
            S3Key=self.s3_filename,
            Publish=True
        )

        logger.info("Created revision {0}".format(response_code['Version']))

        self.update_or_create_alias(response_code['Version'], self.hash_release)
        self.update_or_create_alias(response_code['Version'], alias)

        logger.info("If config wash changed, remember to update function "
                    "configuration")


    def update_or_create_alias(self, version, alias):
        try:
            self.aws_lambda.update_alias(
                FunctionName=self.function_selected,
                FunctionVersion=version,
                Name=alias)
            logger.info("Alias '{0}' updated for version '{1}'".format(
                alias, version
            ))
        except self.aws_lambda.exceptions.ResourceNotFoundException:
            self.aws_lambda.create_alias(
                FunctionName=self.function_selected,
                FunctionVersion=version,
                Name=alias
            )
            logger.info("Alias '{0}' created for version '{1}'".format(
                alias, version
            ))

    def update_function_configuration(self):
        """
            update function configuration without code update
        """

        logger.info("Update function config")
        function_definition = self.get_function_configuration()

        self.aws_lambda.update_function_configuration(
            **function_definition
        )

    def list_aliases(self):
        logger.info("Listing aliases")
        response = self.aws_lambda.list_aliases(
            FunctionName=self.function_selected,
            MaxItems=500

        )
        return response

    def promote_release(self, release):
        """
            update alias "production" to "release"
        """
        logger.info("Updating production alias with revision '{0}'".format(
                    release))
        if release.isdigit() or release == '$LATEST':
            version = release
        else:
            try:
                response = self.aws_lambda.get_alias(
                    FunctionName=self.function_selected,
                    Name=release
                )
                version = response['FunctionVersion']
            except self.aws_lambda.exceptions.ResourceNotFoundException:
                logger.error("Can't found the qualifier {0} for {1}".format(
                    release,
                    self.function_selected
                ))
                return

        self.update_or_create_alias(version, 'production')

    def invoke_sync(self, qualifier, payload):
        """
            Call in sync mode to the function
                payload is a file.
        """
        response =  self.aws_lambda.invoke(
            FunctionName=self.function_selected,
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=payload or bytes(''),
            Qualifier=qualifier
        )
        response['LogResultDecoded'] = base64.decodestring(
            response['LogResult'])
        return response

    def invoke_async(self, revision, payload):
        """
            Call in sync mode to the function
                payload is a file.
        """
        raise NotImplementedError()

    class FunctionNotFoundError(Exception):
        pass
