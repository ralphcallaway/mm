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

def get_data_files(*dirs):
    results = []
    for src_dir in dirs:
        for root,dirs,files in os.walk(src_dir):
            results.append((root, map(lambda f:root + "/" + f, files)))
    return results

setup(
    name='mm',
    version='0.0.1',
    packages=find_packages(),
    py_modules = ['mm'],
    data_files = get_data_files("bin"),
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['mm = mm:main']
    },
    url='https://github.com/joeferraro/mm',
    include_package_data=True,
    author='@joeferraro',
    author_email='info@mavensmate.com',
    description='CLI for MavensMate',
    license='GNU v2',
    keywords='mavensmate salesforce salesorce1 force.com ide cli',
    test_suite='test',
)