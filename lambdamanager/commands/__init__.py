from .create_function import CreateFunction
from .create_release import CreateFunctionRelease
from .list_aliases import ListFunctionAliases

AVAILABLE_COMMANDS = {
    'create': CreateFunction,
    'create_release': CreateFunctionRelease,
    'list_aliases': ListFunctionAliases,
}
