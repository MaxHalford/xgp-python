from __future__ import print_function
import sys
from setuptools import Extension, setup, find_packages

with open('requirements.txt') as f:
    INSTALL_REQUIRES = [l.strip() for l in f.readlines() if l]


try:
    import numpy
except ImportError:
    print('numpy is required during installation')
    sys.exit(1)

try:
    import scipy
except ImportError:
    print('scipy is required during installation')
    sys.exit(1)

setup(name='xgp',
      version='0.0.1',
      description='XGP scikit-learn API',
      author='Max Halford',
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES,
      author_email='maxhalford25@gmail.com',
      url='https://maxhalford.github.io/xgp',
      build_golang={'root': 'github.com/MaxHalford/xgp-sklearn'},
      ext_modules=[Extension('xgp', ['xgp/xgp.go'])],
      setup_requires=['setuptools-golang>=0.2.0'],
      )
