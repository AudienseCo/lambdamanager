from .python27 import Python27LambdaPackage

AVAILABLE_RUNTIMES = {
    'python2.7': {
        'packager': Python27LambdaPackage,
    },
}
