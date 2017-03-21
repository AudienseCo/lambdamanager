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


class LambdaManagerCommand:

    def __init__(self):

        self.command = path.basename(sys.argv[0])
        self.commands = AVAILABLE_COMMANDS
        self.arguments = docopt(
            __doc__.format(
                command=self.command,
                commands='\n'.join([command.__doc__
                                    for (name, command) in self.commands.items()]),
            )
        )

    def __call__(self):

        command = self.arguments['<command>']

        if command == 'help':
            for cmd in self.arguments['<args>']:
                if cmd in self.commands:
                    print(self.commands[cmd].usage().format(command=self.command))
                else:
                    print("{0} is not a valid command".format(cmd))

            exit(0)

        self.config = ConfigYamlReader(self.arguments['--config'])
        self.config.function_properties_check()

        self.aws_lambda = AwsLambdaManager(self.config.config)
        # TODO: Remove this print
