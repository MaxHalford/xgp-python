import numpy as np
from sklearn import multiclass
from sklearn.base import ClassifierMixin
from sklearn import utils

from . import model


class XGPClassifier(model.XGPModel, ClassifierMixin):
    """ XGP classification model."""

    @property
    def default_loss(self):
        return 'logloss'

    def fit(self, X, y, **kwargs):
        if len(np.unique(y)) > 2:
            raise ValueError('Multi-class classification is not supported')

        self = super().fit(X, y, **kwargs)
        return self

    def predict(self, X):
        y_pred = super().predict(X)
        return (y_pred > 0.5).astype(int)

    def predict_proba(self, X):
        y_pred = super().predict(X)
        return 1 / (1 + np.exp(-y_pred))
