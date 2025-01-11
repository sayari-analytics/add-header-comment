"""Setup script for the project."""

import os

from setuptools import find_packages, setup

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(ROOT_DIR, "README.md")) as f:
    DESCRIPTION = f.read()


setup(
    name="add-header-comment",
    version="1.0.0",
    description="Add or update the header of a file with the appropriate comment style.",
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Nathaniel Young",
    author_email="nyoung@sayari.com",
    maintainer="Sayari Labs",
    maintainer_email="",
    license="MIT",
    url="https://github.com/sayari-analytics/add-header-comment",
    project_urls={
        "Bug Tracker": "https://github.com/sayari-analytics/add-header-comment/issues",
        "Source Code": "https://github.com/sayari-analytics/add-header-comment",
    },
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.5",
    entry_points={
        "console_scripts": [
            "add-header = add_header_comment.__main__:main",
            "add-header-comment = add_header_comment.__main__:main",
        ],
    },
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["pre-commit", "file header", "license", "automation"],
)
