from .create_function import CreateFunction
from .create_release import CreateFunctionRelease
from .list_aliases import ListFunctionAliases
from .invoke import InvokeFunction

AVAILABLE_COMMANDS_HANDLERS = (
    CreateFunction,
    CreateFunctionRelease,
    ListFunctionAliases,
    InvokeFunction,
)
