from __future__ import absolute_import, print_function
from os import path
import os
from subprocess import call

from ..basepackager import BasePackager


class Python27LambdaPackage(BasePackager):

    file_extensions = ['.py', '.pyo', '.so']

    def build_code(self):
        """ The way to get bundle dependencies """
        if not path.isfile(path.join(self.tmpdir, 'requirements.txt')):
            return

        oldpwd = os.getcwd()
        os.chdir(self.tmpdir)

        call('pip install --requirement requirements.txt --target .'.split(' '))

        os.chdir(oldpwd)

