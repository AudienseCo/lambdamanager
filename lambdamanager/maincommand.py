"""
Usage: {command} [-c FILE] <command> [<args>...]

-h --help           show this
-c --config FILE    The function config file [default: ./functions.yml ]

These are the available commands:
{commands}

See 'git help <command>' for more information on a specific command.
"""

from __future__ import absolute_import, print_function

import sys
from os import path

from docopt import docopt

from .awslambda import AwsLambdaManager
from .commands import AVAILABLE_COMMANDS
from .configreader import ConfigYamlReader


def _doc_help():
    return __doc__.format(
        command=path.basename(sys.argv[0]),
        commands='\n'.join([command.__doc__
                            for (name, command) in AVAILABLE_COMMANDS.items()]),
    )


class LambdaManagerCommand:

    def __init__(self):

        self.command = path.basename(sys.argv[0])
        self.commands = AVAILABLE_COMMANDS
        self.arguments = docopt(_doc_help())

    def __call__(self):

        command = self.arguments['<command>']

        if command == 'help':
            for cmd in self.arguments['<args>']:
                if cmd in self.commands:
                    print(self.commands[cmd].usage().format(command=self.command))
                else:
                    print("{0} is not a valid command".format(cmd))
            if not self.arguments['<args>']:
                print(_doc_help())
            exit(0)

        elif command not in self.commands:
            print("{0} is not a valid command, see help".format(command))
            exit(1)

        self.config = ConfigYamlReader(self.arguments['--config'])
        self.config.function_properties_check()

        self.aws_lambda = AwsLambdaManager(self.config.config)

        command = self.commands[command](self.aws_lambda)
        exit(command() or 0)
