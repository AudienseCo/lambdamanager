from __future__ import absolute_import, print_function
from ..basecommand import BaseCommand


class UpdateFunctionConfiguration(BaseCommand):
    """ update_config: Update the function configuration """

    subcommand_name = 'update_config'

    def __call__(self, _):
        self.function_must_exists()
        self.aws_lambda.update_function_configuration()
