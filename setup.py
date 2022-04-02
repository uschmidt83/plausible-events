from os import path

from setuptools import find_packages, setup

_dir = path.abspath(path.dirname(__file__))

with open(path.join(_dir, "plausible_events", "version.py"), encoding="utf-8") as f:
    exec(f.read())

with open(path.join(_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="plausible-events",
    version=__version__,
    description="Plausible.io Events API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uschmidt83/plausible-events",
    author="Uwe Schmidt",
    author_email="mail@uweschmidt.org",
    license="BSD 3-Clause License",
    packages=find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=[
        "requests",
        # "miniupnpc",
    ],
)
