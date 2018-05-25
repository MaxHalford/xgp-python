# XGP Python package

[![PyPI version](https://badge.fury.io/py/xgp.svg)](https://badge.fury.io/py/xgp)
[![Travis build status](https://travis-ci.org/MaxHalford/xgp-python.svg?branch=master)](https://travis-ci.org/MaxHalford/xgp-python)
[![Coverage Status](https://coveralls.io/repos/github/MaxHalford/xgp-python/badge.svg?branch=master)](https://coveralls.io/github/MaxHalford/xgp-python?branch=master)

This repository contains Python bindings to the [XGP library](https://github.com/MaxHalford/xgp). It is a simple wrapper that calls the XGP dynamic shared library and exposes a scikit-learn interface.

## Documentation

Please refer to the [Python section of the XGP website](https://maxhalford.github.io/xgp/python/).

## Installation

Installation instructions are available [here](https://maxhalford.github.io/xgp/cli/#installation).

## Quick start

```python
>>> from sklearn import datasets
>>> from sklearn import metrics
>>> from sklearn import model_selection
>>> import xgp

>>> X, y = datasets.load_breast_cancer(return_X_y=True)
>>> X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, random_state=42)

>>> model = xgp.XGPClassifier(
...    loss_metric='logloss',
...    funcs='sum,sub,mul,div',
...    n_individuals=500,
...    n_generations=100,
...    random_state=42,
...    parsimony_coefficient=0.01
... )

>>> model = model.fit(X_train, y_train, eval_set=(X_test, y_test), verbose=True)

>>> metrics.log_loss(y_train, model.predict_proba(X_train))  # doctest: +ELLIPSIS
0.217573...

>>> metrics.log_loss(y_test, model.predict_proba(X_test))  # doctest: +ELLIPSIS
0.191963...

>>> print('Best program:', model.program_str_)  # doctest: +ELLIPSIS
Best program: sum(mul(X[0], mul(-4.774751..., X[7])), 3.876205...)

```

