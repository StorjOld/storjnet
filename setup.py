#!/usr/bin/env python
# coding: utf-8


import os
import sys
from setuptools import setup, find_packages


# Only load py2exe settings when its used, so we can install it first.
options = {}
cmdclass = {}
if os.name == 'nt' and 'py2exe' in sys.argv:
    import py2exe  # NOQA
    from py2exe_MediaCollector import MediaCollector
    options = {'py2exe': {
        "skip_archive": True,
        "dll_excludes": [
            'IPHLPAPI.DLL', 'WTSAPI32.dll', 'CRYPT32.dll',
            'PSAPI.DLL', 'MSVCR100.dll'
        ],
        "optimize": 2,
        "bundle_files": 3,  # This tells py2exe to bundle everything
    }}
    cmdclass = {'py2exe': MediaCollector}


# Only load py2app settings when its used, so we can install it first.
if os.name == 'postix' and 'py2app' in sys.argv:
    import py2app  # NOQA
    options = {'py2app': {
        "optimize": 2,
    }}


exec(open('storjnet/version.py').read())  # load __version__
SCRIPTS = [os.path.join('storjnet', 'bin', 'storjnet')]


setup(
    app=['storjnet/bin/storjnet'],
    name='storjnet',
    description="Storjnet reference implementation.",
    long_description=open("README.rst").read(),
    keywords="storj, reference, protocol, DHT",
    url='http://storj.io',
    author='Fabian Barkhau',
    author_email='f483+storjnet@storj.io',
    license="MIT",
    version=__version__,  # NOQA
    scripts=SCRIPTS,
    console=SCRIPTS,
    dependency_links=[],
    install_requires=open("requirements.txt").readlines(),
    tests_require=open("test_requirements.txt").readlines(),
    packages=find_packages(exclude=['storjnet.bin']),
    classifiers=[
        # "Development Status :: 1 - Planning",
        "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        # "Programming Language :: Python :: 3",
        # "Programming Language :: Python :: 3.3",
        # "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    cmdclass=cmdclass,
    options=options
)
