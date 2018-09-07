from __future__ import print_function
from setuptools import Extension, setup, find_packages

with open('requirements.txt') as f:
    INSTALL_REQUIRES = [l.strip() for l in f.readlines() if l]


setup(
    name='xgp',
    version='0.0.4',
    description='XGP Python package with a scikit-learn interface',
    author='Max Halford',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    author_email='maxhalford25@gmail.com',
    url='https://maxhalford.github.io/xgp',
    build_golang={'root': 'github.com/MaxHalford/xgp-python'},
    ext_modules=[Extension('xgp', ['xgp/xgp.go'])],
    setup_requires=['setuptools-golang>=0.2.0'],
)
