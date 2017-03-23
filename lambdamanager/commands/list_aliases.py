from __future__ import absolute_import, print_function

from ..basecommand import BaseCommand


class ListFunctionAliases(BaseCommand):
    """ list_aliases: List the available aliases for a given function"""

    subcommand_name = 'list_aliases'

    def __call__(self, arguments):

        self.function_must_exists()

        aliases = self.aws_lambda.list_aliases()
        for item in aliases['Aliases']:
            print("{Name} -> {FunctionVersion}".format(**item))
