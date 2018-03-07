"""
 A cli tool too launch, manage and use ethereum client on the cloud
"""
import os
import sys

import re
from setuptools import find_packages, setup


def get_version():
    with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as version_file:
        return version_file.read().strip()


def get_description():
    try:
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except (IOError, ImportError):
        return 'A cli tool to translate comments in source code from one language to another'

version = get_version()
dependencies = []
description = get_description()

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push origin master --tags")
    sys.exit()

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()


setup(
    name='transource',
    version=version,
    url='https://github.com/kgritesh/transource',
    license='MIT',
    author='Ritesh Kadmawala',
    author_email='k.g.ritesh@gmail.com',
    description=' A cli tool to translate comments in source code from one language to another using google translate',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'transource = transource:cli',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
