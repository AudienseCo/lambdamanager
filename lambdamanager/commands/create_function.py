#!/usr/bin/env python
"""
    usage: {command} -c configfile.yml create
"""
from __future__ import absolute_import, print_function

from pprint import pprint
import sys

from docopt import docopt

from ..awslambda import AwsLambdaManager, ConfigYamlReader


class CreateFunction:
    """create: Create lambda functions in AWS service."""
    def __init__(self, manager):
        self.aws_lambda = manager

    @classmethod
    def usage(self):
        """Get the command usage"""
        return "{0}\n{1}\n".format(self.__doc__, __doc__)

    def __call__(self):
        print(docopt(__doc__))
        return
        if not self.aws_lambda.function_exists():
            self.aws_lambda.create_function()
        else:
            print("The function already exists")
            sys.exit(1)
