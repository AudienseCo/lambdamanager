from copy import deepcopy
import yaml
from os import path
import os
from shutil import copytree, rmtree
from tempfile import mkdtemp

import boto3
from git import Repo
from moto import mock_lambda, mock_s3
import pytest

from lambdamanager.awslambda import AwsLambdaManager


FUNCTION_EXAMPLE = {
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

AWS_LAMBDA_CONFIG_ONE_FUNCTION = {
    'function-one': FUNCTION_EXAMPLE,
}

AWS_LAMBDA_CONFIG_FUNCTIONS = {
    'function-one': FUNCTION_EXAMPLE,
    'function-two': FUNCTION_EXAMPLE,
}

FUNCTION_ONE_PATH = path.join(path.dirname(path.dirname(__file__)),
                              'assets/function_sample')

with open(path.join(FUNCTION_ONE_PATH, 'functions.yml'), 'r') as config_file:
    FUNCTION_ONE_CONFIG = yaml.load(config_file)


@mock_lambda
def test_awslambda_init():
    config = {}
    alm = AwsLambdaManager(config)

    assert alm.config == config


@mock_lambda
def test_awslambda_init_config():

    alm = AwsLambdaManager(AWS_LAMBDA_CONFIG_ONE_FUNCTION)

    assert alm.config == AWS_LAMBDA_CONFIG_ONE_FUNCTION


@mock_lambda
def test_awslambda_available_functions():

    alm = AwsLambdaManager(AWS_LAMBDA_CONFIG_ONE_FUNCTION)

    assert 'function-one' in alm.available_functions()


@mock_lambda
def test_awslambda_select_function_default():

    alm = AwsLambdaManager(AWS_LAMBDA_CONFIG_ONE_FUNCTION)

    alm.select_function()

    assert alm.function_selected == 'function-one'


@mock_lambda
def test_awslambda_select_function_from_multiple():

    alm = AwsLambdaManager(AWS_LAMBDA_CONFIG_FUNCTIONS)

    with pytest.raises(AwsLambdaManager.MultipleFunctionsFoundError):
        alm.select_function()

    alm.select_function('function-two')
    assert alm.function_selected == 'function-two'

    with pytest.raises(AwsLambdaManager.FunctionNotFoundError):
        alm.select_function('not-valid-function')


@mock_lambda
def test_awslambda_get_function_configuration_ok():

    alm = AwsLambdaManager(AWS_LAMBDA_CONFIG_ONE_FUNCTION)
    alm.select_function()

    function_config = alm.get_function_configuration()
    # Check required keys are present:
    for key in ('FunctionName', 'Runtime', 'Role', 'Handler', 'MemorySize'):
        assert key in function_config

    # Check not required keys are present:
    for key in ('Environment', 'Description', 'Timeout', 'VpcConfig'):
        assert key in function_config


@mock_lambda
def test_awslambda_get_function_configuration_mininal():

    config = deepcopy(FUNCTION_EXAMPLE)
    for key in ('Environment', 'Description', 'Timeout', 'VpcConfig'):
        del config[key]

    alm = AwsLambdaManager({'function-one': config})
    alm.select_function()

    function_config = alm.get_function_configuration()
    # Check required keys are present:
    for key in ('FunctionName', 'Runtime', 'Role', 'Handler', 'MemorySize'):
        assert key in function_config

    # Check not required keys are not present:
    for key in ('Environment', 'Description', 'Timeout', 'VpcConfig'):
        assert key not in function_config


@mock_lambda
def test_awslambda_create_package_config_ok():

    # Temporary asset creation
    tmpdir = mkdtemp(prefix='lambdamanagertest')
    function_basename = path.basename(FUNCTION_ONE_PATH)
    copytree(FUNCTION_ONE_PATH, path.join(tmpdir, function_basename))
    oldpwd = os.getcwd()
    os.chdir(path.join(tmpdir, function_basename))

    # Create a repo structure
    tmprepo = Repo.init('.')
    open('GIT_FILE', 'w').close()
    tmprepo.index.add(['GIT_FILE'])
    tmprepo.index.commit('sad initial commit')

    alm = AwsLambdaManager(FUNCTION_ONE_CONFIG)
    alm.select_function('function-one')
    alm.create_package(release_tag='test')

    assert path.getsize(alm.local_filename) > 128
    assert path.isfile(alm.local_filename)

    # test extra tearDown ...
    os.chdir(oldpwd)
    rmtree(tmpdir)

# TODO: Implement a helper to create more tests about packaging.
# Including something about Runtime selection.


@mock_lambda
@mock_s3
def test_awslambda_upload_package_ok():

    # Temporary asset creation
    tmpdir = mkdtemp(prefix='lambdamanagertest')
    function_basename = path.basename(FUNCTION_ONE_PATH)
    copytree(FUNCTION_ONE_PATH, path.join(tmpdir, function_basename))
    oldpwd = os.getcwd()
    os.chdir(path.join(tmpdir, function_basename))

    # Create a repo structure
    tmprepo = Repo.init('.')
    open('GIT_FILE', 'w').close()
    tmprepo.index.add(['GIT_FILE'])
    tmprepo.index.commit('sad initial commit')

    alm = AwsLambdaManager(FUNCTION_ONE_CONFIG)
    alm.select_function('function-one')
    alm.create_package(release_tag='test')

    alm.upload_package()

    s3 = boto3.resource('s3')
    mocked_obj = s3.Object(
        FUNCTION_ONE_CONFIG['function-one']['Code']['S3Bucket'],
        path.join(FUNCTION_ONE_CONFIG['function-one']['Code']['S3KeyPath'],
                  alm.local_filename)
    ).get()

    assert path.getsize(alm.local_filename) > 0
    assert mocked_obj['ContentLength'] == path.getsize(alm.local_filename)

    # test extra tearDown ...
    os.chdir(oldpwd)
    rmtree(tmpdir)


@mock_lambda
@mock_s3
def test_awslambda_create_function_ok():
    # TODO: To be implemented
    assert True


@mock_lambda
def test_awslambda_function_exists_exists():
    # TODO: To be implemented
    assert True


@mock_lambda
def test_awslambda_function_exists_not_exists():
    # TODO: To be implemented
    assert True


@mock_lambda
@mock_s3
def test_awslambda_create_release():
    # TODO: To be implemented
    assert True


@mock_lambda
def test_awslambda_update_or_create_alias_update():
    # TODO: To be implemented
    assert True


@mock_lambda
def test_awslambda_update_or_create_alias_create():
    # TODO: To be implemented
    assert True


@mock_lambda
def test_awslambda_update_or_create_alias_failed():
    # TODO: To be implemented
    assert True


@mock_lambda
def test_awslambda_update_function_configuration_ok():
    # TODO: To be implemented
    assert True


@mock_lambda
def test_awslambda_update_function_configuration_failed():
    # TODO: To be implemented
    assert True


@mock_lambda
def test_awslambda_list_aliases_ok():
    # TODO: To be implemented
    assert True


@mock_lambda
def test_awslambda_list_aliases_failed():
    # TODO: To be implemented
    assert True


@mock_lambda
def test_awslambda_promote_release_ok():
    # TODO: To be implemented
    assert True


@mock_lambda
def test_awslambda_promote_release_failed():
    # TODO: To be implemented
    assert True


@mock_lambda
def test_awslambda_invoke_sync_ok():
    # TODO: To be implemented
    assert True


@mock_lambda
def test_awslambda_invoke_sync_failed():
    # TODO: To be implemented
    assert True


@mock_lambda
def test_awslambda_invoke_async_ok():
    # TODO: To be implemented
    assert True


@mock_lambda
def test_awslambda_invoke_async_failed():
    # TODO: To be implemented
    assert True
