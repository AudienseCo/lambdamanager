import sys
from os import path

class BaseCommand(object):

    command_doc = __doc__
    EXIT_OK = 0
    EXIT_GENERIC_FAILURE = 1

    subcommand_name = 'base'
    extra_args = ''
    extra_args_body = ''

    def __init__(self, manager):
        self.aws_lambda = manager

    @classmethod
    def usage(self):
        """Formated usage"""
        return "{0}\n{1}\n".format(self.__doc__, self.command_usage())

    @classmethod
    def command_usage(self):
        return """
Usage: {command} [-c CONFIGFILE] {subcommand} [<function_name>] {extra_args}

    If there are more than one function in configfile.yml, then
    function_name is mandatory

-h --help           show this
-c CONFIGFILE, --config=CONFIGFILE    The function config file [default: ./functions.yml]
{extra_args_body}
""".format(
            command=path.basename(sys.argv[0]),
            subcommand=self.subcommand_name,
            extra_args=self.extra_args,
            extra_args_body=self.extra_args_body)

    def select_function(self, function_name):
        """A simple helper to select the current function"""

        if not function_name:
            if len(self.aws_lambda.available_functions()) > 1:
                print("There are more than one function in the file, please select"
                      " one")
                exit(self.EXIT_GENERIC_FAILURE)
            else:
                self.aws_lambda.select_function()

        else:
            self.aws_lambda.select_function(function_name)

    def function_must_exists(self):
        if not self.aws_lambda.function_exists():
            print("Lambda function not found")
            exit(self.EXIT_GENERIC_FAILURE)

    def __call__(self, arguments):
        raise NotImplementedException()
