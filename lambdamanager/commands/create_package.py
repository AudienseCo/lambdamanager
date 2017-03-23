from ..basecommand import BaseCommand


class CreateFunctionPackage(BaseCommand):
    """ create_package: create the zip package without publish it """

    subcommand_name = 'create_package'
    extra_args = '[<alias_name>]'
    extra_args_body = " alias_name value is devel by default"

    def __call__(self, arguments):
        self.aws_lambda.create_package(arguments['<alias_name>'] or 'devel')
        print("The package name is: {0}".format(
            self.aws_lambda.local_filename)
        )
