"""Setup"""
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    README = fh.read()

setup(
    name="reretrieve",
    version="0.0.0.dev4",
    author="Salomon Smeke Cohen",
    author_email="salomon@ssmeke.io",
    description="A regex storage and retrieval tool",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SalomonSmeke/rere",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Framework :: tox",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    keywords="regex storage search retrieval cli",
    project_urls={
        "Author": "https://ssmeke.io",
        "Source": "https://github.com/SalomonSmeke/rere",
        "Tracker": "https://github.com/SalomonSmeke/rere/issues",
        "Donations": "https://paypal.me/ssmeke",
    },
    python_requires=">=3.6",
    install_requires=["mypy", "urllib3"],
    entry_points={
        "pytest11": ["tox_tested_package=tox_tested_package.fixtures"],
        "console_scripts": ["rere=src.entry:main"],
    },
)
