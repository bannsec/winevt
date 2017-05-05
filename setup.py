# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
#with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()
long_description = "See website for more info."

setup(
    name='winevt',
    version='0.0.1',
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
    install_requires=["cffi>=1.0.0"],
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["winevt/winevt_build.py:ffibuilder"],
    extras_require={
        'dev': ['ipython'],
    },

)

