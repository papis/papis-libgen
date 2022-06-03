# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.rst') as fd:
    long_description = fd.read()

setup(
    name='papis-libgen',
    version='0.1.1',
    author='Alejandro Gallo',
    author_email='aamsgallo@gmail.com',
    license='GPLv3',
    url='https://github.com/papis/papis-libgen',
    install_requires=[
        "papis>=0.12",
        # TODO: check if later versions also work,
        #       version 2.0 only works for py 3.6 and above
        "pylibgen==1.3.1",
    ],
    classifiers=[],
    description='Libgen plugin for papis',
    long_description=long_description,
    extras_require=dict(
        develop=[
            "sphinx",
            'sphinx-click',
            'sphinx_rtd_theme',
            'pytest',
            'pytest-cov',
        ]
    ),
    keywords=[
        'papis', 'libgen', 'bibtex',
        'management', 'cli', 'biliography'
    ],
    packages=[
        "papis_libgen",
    ],
    entry_points={
        'papis.downloader': [
            "libgen=papis_libgen:Downloader",

        ],
        'papis.explorer': [
            "libgen=papis_libgen:explorer",

        ]
    }
)
