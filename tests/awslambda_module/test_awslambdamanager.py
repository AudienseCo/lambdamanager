from moto import mock_lambda
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
