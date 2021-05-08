import sys
import os

if sys.version_info[0] < 3:
    print("Python version detected:\n*****\n{0!s}\n*****\nCannot run, must be using Python 3".format(sys.version))
    sys.exit()

from setuptools import setup, find_packages
from glob import glob


def find_scripts(pkgnames):
    ret = []
    for pkgname in pkgnames:
        for item in os.walk(pkgname):
            _, last = os.path.split(item[0])
            if last == "scripts":
                ret.extend(glob(os.path.join(item[0], '*.py')))
    return ret


PACKAGE_NAME = "f312"

pkgs = find_packages()
scripts = find_scripts([PACKAGE_NAME])

setup(
    name=PACKAGE_NAME,
    packages=find_packages(),
    include_package_data=True,
    version='19.6.27.0',
    license='GNU GPLv3',
    platforms='any',
    description='Framework to implement file readers/writers',
    author='Julio Trevisan',
    author_email='juliotrevisan@gmail.com',
    url='https://github.com/trevisanj/f312',
    keywords= [],
    install_requires=[],
    scripts=scripts
)

