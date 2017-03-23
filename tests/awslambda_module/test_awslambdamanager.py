from lambdamanager.awslambda import AwsLambdaManager
from moto import mock_lambda


@mock_lambda
def test_awslambda_init():
    config = {}
    alm = AwsLambdaManager(config)

    assert alm.config == config
