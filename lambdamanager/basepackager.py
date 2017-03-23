from os import path
import os
import zipfile
import shutil
from tempfile import mkdtemp
import re


class BasePackager(object):

    file_extensions = []

    def __init__(self, package_name, release, source_directory,
                 target_directory='.'):

        self.package_name = package_name
        self.release = release
        self.source_directory = source_directory
        self.target_directory = target_directory

        self.filename = "{package_name}-{release}.zip".format(
            target_directory=target_directory,
            package_name=package_name,
            release=release)

        self.base_tmpdir = mkdtemp(prefix='lambda-{}'.format(package_name))
        self.tmpdir = path.join(self.base_tmpdir, self.package_name)

    def build_and_save(self, extra_files=[]):

        self.zipf = zipfile.ZipFile(
            path.join(self.target_directory, self.filename),
            'w',
            zipfile.ZIP_DEFLATED)

        self.copy_files(self.source_directory)
        self.build_code()
        self.add_files()

        self.zipf.writestr('PACKAGE_NAME', self.package_name)
        self.zipf.writestr('RELEASE', self.release)

        self.zipf.close()
        # shutil.rmtree(self.base_tmpdir)

    def build_code(self):
        """ The way to get bundle dependencies """
        raise NotImplementedError('build_code is not implemented')

    def copy_files(self, source_directory):
        """ Copy files from directory to tmpdir """
        oldpwd = os.getcwd()
        os.chdir(source_directory)

        shutil.copytree('.', self.tmpdir)

        os.chdir(oldpwd)

    def add_files(self):
        """ Add the files in the temporary directory to the zip"""
        oldpwd = os.getcwd()
        os.chdir(self.tmpdir)

        for (current_dir, directories, files) in os.walk('.', topdown=False):
            valid_files = filter(lambda f:
                                 re.search('({})$'.format(
                                     '|'.join(self.file_extensions)), f),
                                 files)
            for valid_file in valid_files:
                self.zipf.write(path.join(current_dir, valid_file))

        os.chdir(oldpwd)
