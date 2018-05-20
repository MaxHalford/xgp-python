from sklearn.base import RegressorMixin

from . import model


class XGPRegressor(model.XGPModel, RegressorMixin):
    """ XGP regression model."""

    @property
    def default_loss(self):
        return 'mae'
