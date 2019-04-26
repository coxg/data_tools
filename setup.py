from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='data_tools',
    version='0.21',
    description='Tools for data engineers',
    url='https://github.com/coxg/data_tools',
    author='Gaven Cox',
    author_email='gavencox@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['data_tools']
)
