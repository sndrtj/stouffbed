"""
setup.py
~~~~~~~~~~~~~
:copyright: (c) 2017 Sander Bollen
:copyright: (c) 2017 Leiden University Medical Center
:license: MIT
"""
from os.path import abspath, dirname, join

from setuptools import setup

from stouffbed import __version__


readme_file = join(abspath(dirname(__file__)), "readme.md")
with open(readme_file) as desc_handle:
    long_desc = desc_handle.read()


setup(
    name="stouffbed",
    version=__version__,
    description="Calculate Stouffer's Z-scores from bed files",
    author="Sander Bollen",
    license="MIT",
    install_requires=[
        "click",
        "numpy"
    ],
    entry_points={
        "console_scripts": [
            "stouffbed = stouffbed.cli:main"
        ]
    },
    classifiers=[
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ]
)
