"""
Usage: {command} [-c FILE] <command> [<args>...]

-h --help           show this
-c --config FILE    The function config file [default: ./functions.yml]

These are the available commands:

{commands}

See '{command} help <command>' for more information on a specific command.
"""

from __future__ import absolute_import, print_function

import sys
from os import path

from docopt import docopt

from .awslambda import AwsLambdaManager
from .commands import AVAILABLE_COMMANDS_HANDLERS
from .configreader import ConfigYamlReader


def _doc_help():
    return __doc__.format(
        command=path.basename(sys.argv[0]),
        commands='\n'.join([cmd.__doc__
                            for cmd in AVAILABLE_COMMANDS_HANDLERS]),
    )


class LambdaManagerCommand:

    def __init__(self):

        self.command = path.basename(sys.argv[0])

        self.commands = {
            handler.subcommand_name: handler
            for handler in AVAILABLE_COMMANDS_HANDLERS
        }

        self.main_arguments = docopt(_doc_help(), options_first=True)

    def __call__(self):

        command = self.main_arguments['<command>']

        if command == 'help':
            for cmd in self.main_arguments['<args>']:
                if cmd in self.commands:
                    print(self.commands[cmd].command_usage())
                else:
                    print("{0} is not a valid command".format(cmd))
            if not self.main_arguments['<args>']:
                print(_doc_help())
            exit(0)

        elif command not in self.commands:
            print("{0} is not a valid command, see help".format(command))
            exit(1)

        arguments = docopt(self.commands[command].command_usage())

        self.config = ConfigYamlReader(arguments['--config'])
        self.config.configfile_check()

        self.aws_lambda = AwsLambdaManager(self.config.config)
        self.aws_lambda.select_function(arguments.get('<function_name>'))

        command = self.commands[command](self.aws_lambda)
        exit(command(arguments) or 0)
