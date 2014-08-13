import re
import os
import codecs

from setuptools import setup, find_packages

def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='mm',
    version='0.0.1',
    package_dir = {'': 'lib'},
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['mm = mm:main']
    },
    include_package_data=True,
    author='@joeferraro',
    author_email='info@mavensmate.com',
    description='CLI for MavensMate',
    license='Apache v2',
    keywords='mavensmate salesforce salesorce1 force.com ide cli',
    url='http://mavensmate.com/',
    test_suite='test',
)