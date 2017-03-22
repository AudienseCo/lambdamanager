from __future__ import absolute_import, print_function

from ..basecommand import BaseCommand

from pprint import pprint

class PromoteFunctionRelease(BaseCommand):
    """ promote_release: Update the alias named 'production' """

    subcommand_name = 'promote_release'
    extra_args = '[<release_qualifier>]'
    extra_body = "  release_qualifier is version or alias [default: devel]"

    def __call__(self, arguments):
        qualifier = arguments['<release_qualifier>'] or 'devel'

        self.function_must_exists()
        response = self.aws_lambda.promote_release(qualifier)
        pprint(response)
