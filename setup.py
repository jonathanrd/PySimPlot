# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='PySimPlot',
    version='0.1.1',
    description='PySimPlot',
    author='Jonathan Davies',
    author_email='jonathanrd@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["PySimPlot"],
    install_requires = ["matplotlib>=3.5.0"],
    entry_points={
    'console_scripts': ['pysimplot = PySimPlot.cmd:main']
    },
    python_requires=">=3.6"
)
