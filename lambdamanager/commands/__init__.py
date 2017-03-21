from .create_function import CreateFunction
from .create_release import CreateFunctionRelease

AVAILABLE_COMMANDS = {
    'create': CreateFunction,
    'create_release': CreateFunctionRelease
}
