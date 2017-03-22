from __future__ import absolute_import, print_function

import sys
from os import path

from ..basecommand import BaseCommand


class ListFunctionAliases(BaseCommand):
    """ list_aliases: List the available aliases for a given function"""

    @classmethod
    def command_usage(self):
        return(
"""
usage: {command} [-c FILE] list_aliases [<function_name>]

        If there are more than one function in configfile.yml, then
            function_name is mandatory

""")

    def __call__(self, *args, **kwargs):

        function_name = None
        if len(args) == 1:
            function_name = args[0]

        self.select_function(function_name)

        if not self.aws_lambda.function_exists():
            print("The function doesn't exist")
            sys.exit(self.EXIT_GENERIC_FAILURE)

        aliases = self.aws_lambda.list_aliases()
        for item in aliases['Aliases']:
            print("{Name} -> {FunctionVersion}".format(**item))
