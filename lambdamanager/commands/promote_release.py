from __future__ import absolute_import, print_function

from ..basecommand import BaseCommand


class PromoteFunctionRelease(BaseCommand):
    """ promote_release: Update the alias named 'production' """

    subcommand_name = 'promote_release'
    extra_args = '[<release_qualifier>]'
    extra_body = "  release_qualifier is version or alias [default: devel]"

    def __call__(self, arguments):
        qualifier = arguments['<release_qualifier>'] or 'devel'

        if self.aws_lambda.function_exists():
            return(self.aws_lambda.promote_release(qualifier))
        else:
            print("Lambda function not found")
            return(self.EXIT_GENERIC_FAILURE)
