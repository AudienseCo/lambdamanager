from .create_function import CreateFunction
from .create_release import CreateFunctionRelease
from .list_aliases import ListFunctionAliases
from .invoke import InvokeFunction
from .promote_release import PromoteFunctionRelease
from .update_function_configuration import UpdateFunctionConfiguration

AVAILABLE_COMMANDS_HANDLERS = (
    CreateFunction,
    CreateFunctionRelease,
    ListFunctionAliases,
    InvokeFunction,
    PromoteFunctionRelease,
    UpdateFunctionConfiguration,
)
