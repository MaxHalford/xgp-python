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

>>> X, y = datasets.load_boston(return_X_y=True)
>>> X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, random_state=42)

>>> model = xgp.XGPRegressor(
...    flavor='boosting',
...    loss_metric='mse',
...    funcs='add,sub,mul,div',
...    n_individuals=50,
...    n_generations=20,
...    parsimony_coefficient=0.01,
...    n_rounds=8,
...    random_state=42,
... )

>>> model = model.fit(X_train, y_train, eval_set=(X_test, y_test), verbose=True)

>>> metrics.mean_squared_error(y_train, model.predict(X_train))  # doctest: +ELLIPSIS
17.794685...

>>> metrics.mean_squared_error(y_test, model.predict(X_test))  # doctest: +ELLIPSIS
17.337693...

```

This will also produce the following output in the shell:

```sh
00:00:00 -- train mse: 42.06567 -- val mse: 33.80606 -- round 1
00:00:00 -- train mse: 24.20662 -- val mse: 22.73832 -- round 2
00:00:00 -- train mse: 22.06328 -- val mse: 18.90887 -- round 3
00:00:00 -- train mse: 20.25549 -- val mse: 18.45531 -- round 4
00:00:00 -- train mse: 18.86693 -- val mse: 18.22908 -- round 5
00:00:00 -- train mse: 17.79469 -- val mse: 17.33769 -- round 6
00:00:01 -- train mse: 17.62692 -- val mse: 22.67012 -- round 7
00:00:01 -- train mse: 17.24799 -- val mse: 22.77802 -- round 8
```
