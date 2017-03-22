from __future__ import absolute_import, print_function

import sys
from os import path

from ..basecommand import BaseCommand


class ListFunctionAliases(BaseCommand):
    """ list_aliases: List the available aliases for a given function"""

    subcommand_name = 'list_aliases'

    def __call__(self, arguments):

        if not self.aws_lambda.function_exists():
            print("The function doesn't exist")
            sys.exit(self.EXIT_GENERIC_FAILURE)

        aliases = self.aws_lambda.list_aliases()
        for item in aliases['Aliases']:
            print("{Name} -> {FunctionVersion}".format(**item))
