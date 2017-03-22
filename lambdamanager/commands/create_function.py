from __future__ import absolute_import, print_function

import sys
from os import path

from ..basecommand import BaseCommand


class CreateFunction(BaseCommand):
    """ create: Create lambda functions in AWS service."""

    subcommand_name = 'create'

    def __call__(self, arguments):

        print(self.aws_lambda.function_selected)
        return self.EXIT_OK

        if not self.aws_lambda.function_exists():
            self.aws_lambda.create_function()
        else:
            print("The function already exists")
            return self.EXIT_GENERIC_FAILURE
        return self.EXIT_OK
