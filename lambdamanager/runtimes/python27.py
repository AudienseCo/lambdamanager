from os import path
import os
import zipfile


class Python27LambdaPackage:

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

        self.zipf = zipfile.PyZipFile(
            path.join(target_directory, self.filename),
            'w',
            zipfile.ZIP_DEFLATED)
        self.zipf.writestr('PACKAGE_NAME', package_name)
        self.zipf.writestr('RELEASE', release)

    def add_pyfiles(self):
        oldpwd = os.getcwd()
        os.chdir(path.basename(self.source_directory))
        self.zipf.writepy('.')
        os.chdir(oldpwd)

    def add_otherfiles(self, files):
        for filename in files:
            self.zipf.write(filename)

    def save(self):
        self.zipf.close()
