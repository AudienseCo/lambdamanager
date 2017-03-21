from __future__ import absolute_import, print_function

import sys

from ..basecommand import BaseCommand


class CreateFunction(BaseCommand):
    """create: Create lambda functions in AWS service."""

    command_doc = __doc__

    @classmethod
    def command_usage(self):
        return(
"""
    usage: {command} -c configfile.yml create
""")

    def __call__(self):

        if not self.aws_lambda.function_exists():
            self.aws_lambda.create_function()
        else:
            print("The function already exists")
            sys.exit(1)
        return self.EXIT_OK
