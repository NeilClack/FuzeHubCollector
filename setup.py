from platform import java_ver
from setuptools import setup, find_packages

setup(
    name='FuzeHubCollector',
    version='0.1',
    description='Scrapy Spider for Print Models fueling the FuzeHub',
    author='Neil Clack',
    packages=find_packages(exclude=['*tests*'])
)
