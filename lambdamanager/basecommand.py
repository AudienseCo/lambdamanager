
class BaseCommand(object):

    command_doc = __doc__
    EXIT_OK = 0
    EXIT_GENERIC_FAILURE = 1

    def __init__(self, manager):
        self.aws_lambda = manager

    @classmethod
    def usage(self):
        """Formated usage"""
        return "{0}\n{1}\n".format(self.__doc__, self.command_usage())

    @classmethod
    def command_usage(self):
        """Get the command usage"""
        raise NotImplementedException()

    def __call__(self, *args, **kwargs):
        raise NotImplementedException()
