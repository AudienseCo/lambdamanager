from __future__ import absolute_import, print_function

import sys
from os import path

from ..basecommand import BaseCommand


class CreateFunctionRelease(BaseCommand):
    """ create_release: Create a new release for the selected lambda function"""

    subcommand_name = 'create_release'
    extra_args = '[<release_alias>]'
    extra_body = "  release_alias [default: devel]"

    def __call__(self, arguments):

        alias = arguments['<release_alias>'] or 'devel'

        if self.aws_lambda.function_exists():
            response = self.aws_lambda.create_release(alias)

        else:
            print("Lambda function not found")
            exit(self.EXIT_GENERIC_FAILURE)
