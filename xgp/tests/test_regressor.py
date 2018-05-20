from sklearn.utils.estimator_checks import check_estimator

import xgp


def test_regressor_check_estimator():
    return check_estimator(xgp.XGPRegressor)
