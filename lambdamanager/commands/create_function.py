from __future__ import absolute_import, print_function

import sys
from os import path

from ..basecommand import BaseCommand


class CreateFunction(BaseCommand):
    """create: Create lambda functions in AWS service."""

    command_doc = __doc__

    @classmethod
    def command_usage(self):
        return(
"""
usage: {command} [-c FILE] create [<function_name>]

        If there are more than one function in configfile.yml, then
            function_name is mandatory

""")

    def __call__(self, *args, **kwargs):

        function_name = None
        if len(args) == 1:
            function_name = args[0]

        self.select_function(function_name)

        return self.EXIT_OK

        if not self.aws_lambda.function_exists():
            self.aws_lambda.create_function()
        else:
            print("The function already exists")
            return self.EXIT_GENERIC_FAILURE
        return self.EXIT_OK
