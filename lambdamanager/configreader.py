import yaml

from .runtimes import AVAILABLE_RUNTIMES


class ConfigException(AssertionError):
    pass


class ConfigYamlReader:
    # Config is in yaml format
    def __init__(self, configfile):
        """
        the_visible_lambda_function_name:
            Runtime: python2.7
            Role: a-iam-role
            Handler: module_name.lambda_handler
            Description: A function description  # optional
            Code:
               S3Bucket: the-bucket-name-to-upload-releases
               S3KeyPath: route/to/releases/directory
               Directory: path/to/code/directory
            MemorySize: 128
            Timeout: 120  # optional
            VpcConfig:  # optional
                SubnetIds:
                    - string
                SecurityGroupIds:
                    - string
            Environment:  # optional
                Variables:
                    KEY1: VALUE1
                    KEY2: VALUE2
                    KEY3: VALUE3
        """
        self.configfile = configfile
        with open(self.configfile, 'r') as f:
            self.config = yaml.load(f)

    def configfile_check(self):
        """
        Check the schema
        """
        for (f, fconf) in self.config.items():
            assert 'Runtime' in fconf, ConfigException('Runtime is not defined')
            assert fconf['Runtime'] in AVAILABLE_RUNTIMES, ConfigException('Runtime not available')

