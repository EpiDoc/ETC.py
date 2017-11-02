from setuptools import setup, find_packages
from chetc import __VERSION__

setup(
    name='chetc',
    version=__VERSION__,
    packages=find_packages(exclude=["tests"]),
    url='https://github.com/EpiDoc/ETC.py/',
    license='GNU GPL v2',
    author='Thibault Clérice',
    author_email='leponteineptique@gmail.com',
    description='Converter from plain text Leiden convention to Epidoc XML',
    test_suite="tests"
)
