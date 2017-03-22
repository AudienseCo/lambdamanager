
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

    def __call__(self, *args, **kwargs):
        raise NotImplementedException()
