from __future__ import absolute_import, print_function

from pprint import pprint
from os import path
import sys

from ..basecommand import BaseCommand


class InvokeFunction(BaseCommand):
    """ invoke: Execute the remote function code """

    subcommand_name = 'invoke'
    extra_args = '[--payload=FILE] [--async] [--qualifier=QUALIFIER]'
    extra_args_body = '\n'.join([
        "--async    To launch the function in the async way.",
        "--payload FILE   The filename with the payload to send to the function.",
        "--qualifier QUALIFIER    The alias or function version number [default: devel]",
        "",
        "   Note: If payload is not defined, then taking payload from stdin",
        "   You can do:",
        "   {command} {subcommand} --qualifier alias < payload.json",
    ])

    def __call__(self, arguments):

        if not self.aws_lambda.function_exists():
            print("Lambda function does not exists")
            exit(1)
        qualifier = arguments['--qualifier']
        payload_filename = arguments['--payload']

        func = (self.aws_lambda_invoke_async
                if arguments['--async']
                else self.aws_lambda.invoke_sync)

        if payload_filename and path.isfile(payload_filename):
            payload = open(payload_filename, 'r')
        else:
            payload = sys.stdin

        pprint(func(qualifier, payload))

        if payload_filename:
            payload.close()
