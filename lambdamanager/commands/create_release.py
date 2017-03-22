from __future__ import absolute_import, print_function

import sys
from os import path

from ..basecommand import BaseCommand


class CreateFunctionRelease(BaseCommand):
    """ create_release: Create a new release for the selected lambda function"""

    @classmethod
    def command_usage(self):
        return(
"""
usage: {command} [-c FILE] create_release [<function_name>] [<release_alias>]

        If there are more than one function in configfile.yml, then
            function_name is mandatory

        release_alias is 'devel' by default.

""")

    def __call__(self, *args, **kwargs):

        alias = 'devel'
        function_name = None

        if len(args) == 2:
            alias = self.args[1]
            function_name = self.args[0]
        elif len(args) == 1:
            alias = self.args[0]

        self.select_function(function_name)

        if self.aws_lambda.function_exists():
            response = self.aws_lambda.create_release(self.alias)

        else:
            print("Lambda function not found")
            sys.exit(1)
