"""Setup script for the project."""

import os

from setuptools import find_packages, setup

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(ROOT_DIR, "README.md")) as f:
    DESCRIPTION = f.read()


setup(
    name="add-header",
    version="1.0.0",
    description="Add or update the header of a file.",
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/sayari-analytics/pre-commit-add-header",
    project_urls={
        "Bug Tracker": "https://github.com/sayari-analytics/pre-commit-add-header/issues",
        "Source Code": "https://github.com/sayari-analytics/pre-commit-add-header",
    },
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.5",
    entry_points={
        "console_scripts": [
            "add-header = add_header.__main__:main",
        ],
    },
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["pre-commit", "file header", "license", "automation"],
)
