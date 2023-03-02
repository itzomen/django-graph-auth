#!/usr/bin/env python

import io
import os
import re
from collections import OrderedDict

from setuptools import find_packages, setup


def get_version(package):
    with io.open(os.path.join(package, "__init__.py")) as f:
        pattern = r'^__version__ = [\'"]([^\'"]*)[\'"]'
        return re.search(pattern, f.read(), re.MULTILINE).group(1)


tests_require = [
    "pytest>=3.6.3",
    "pytest-cov>=2.4.0",
    "pytest-django>=3.1.2",
    "coveralls",
]

dev_requires = ["black==22.12.0", "flake8==6.0.0"] + tests_require

setup(
    name="django-graph-auth",
    version=get_version("graph_auth"),
    license="MIT",
    description="Graphql and relay (coming soon) authentication with Graphene for Django.",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    author="itzomen",
    author_email="peng@traleor.com",
    maintainer="itzomen",
    url="https://github.com/itzomen/django-graph-auth",
    project_urls=OrderedDict(
        (
            ("Documentation", "https://github.com/itzomen/django-graph-auth"),
            ("Issues", "https://github.com/itzomen/django-graph-auth/issues"),
        )
    ),
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "Django>=4.1.7",
        "django-graphql-jwt>=0.3.4,<0.4.0",
        "django-filter>=22.1",
        "graphene_django>=3.0.0",
        "graphene>=3.2.1",
    ],
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 4.1",
    ],
    keywords="api graphql rest relay graphene auth",
    zip_safe=False,
    include_package_data=True,
    extras_require={"test": tests_require, "dev": dev_requires},
)
