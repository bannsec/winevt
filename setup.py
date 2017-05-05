import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("setup.py")


# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os
from setuptools.command.install import install
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist
import shutil
from glob import glob
import sys

here = os.path.abspath(os.path.dirname(__file__))

def _build_ffi():
    # This dance is hackish. Probably better way to do this.

    # chdir so we know where we're importing from
    old_dir = os.path.abspath(os.curdir)
    os.chdir(os.path.join(here,"winevt"))

    # Apprently sdist doesn't have "." added by default?
    sys.path.append(".")

    # Try compile it, but be OK with failure
    try:
        # Import our ffi builder
        from winevt_build import ffibuilder

        ffibuilder().compile()
        shutil.copyfile(glob("_winevt.*.pyd")[0],"_winevt.pyd")
    except Exception as e:
        raise Exception(e)
        pass

    # Put us back in our original directory
    os.chdir(old_dir)


class CustomBuildPyCommand(build_py):
    """ Handle generating pyd file but not erroring if we can't. """
    def run(self):
        self.execute(_build_ffi, (), msg='Building ffi')
        build_py.run(self)

class CustomSdistCommand(sdist):
    """ Make sure we generate a new pyd when creating our sdist. """
    def run(self):
        self.execute(_build_ffi, (), msg='Building ffi')
        sdist.run(self)


# Get the long description from the README file
#with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()
long_description = "See website for more info."

setup(
    name='winevt',
    version='0.0.2',
    description='Script to programmatically interface with Windows Events.',
    long_description=long_description,
    url='https://github.com/owlz/winevt',
    author='Michael Bann',
    author_email='self@bannsecurity.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
        'Environment :: Console'
    ],
    keywords='windows event evt evtx',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=["cffi>=1.0.0","untangle"],
    setup_requires=["cffi>=1.0.0"],
    #cffi_modules=["winevt/winevt_build.py:ffibuilder"],
    extras_require={
        'dev': ['ipython'],
    },
    cmdclass={
        #'install': CustomInstallCommand,
        'build_py': CustomBuildPyCommand,
        'sdist': CustomSdistCommand,
    },
    package_data={'winevt': ['_winevt.pyd']},
)

