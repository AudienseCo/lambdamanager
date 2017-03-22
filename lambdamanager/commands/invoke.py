from __future__ import absolute_import, print_function

from pprint import pprint
import sys

from ..basecommand import BaseCommand


class InvokeFunction(BaseCommand):
    """ invoke: Execute the remote function code """

    subcommand_name = 'invoke'
    extra_args = '[--async] [--qualifier=QUALIFIER] [--payload=PAYLOAD_FILE]'
    extra_args_body = '\n'.join([
        "--async    To launch the function in the async way.",
        "--qualifier QUALIFIER    The alias or function version number [default: devel]",
        "--payload PAYLOAD_FILE     The file with the payload to send to the function.",
    ])

    def __call__(self, arguments):

        print(arguments)
        return

        if not self.aws_lambda.function_exists():
            print("Lambda function does not exists")
            sys.exit(1)

        qualifier = arguments['--qualifier']

        func = (self.aws_lambda_invoke_async
                if self.options.async
                else self.aws_lambda.invoke_sync)

        return func(str(qualifier), self.options.payload)
