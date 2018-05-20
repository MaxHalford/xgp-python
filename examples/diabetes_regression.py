from sklearn import datasets
from sklearn import metrics
import xgp


X, y = datasets.load_boston(return_X_y=True)

model = xgp.XGPRegressor(
    loss_metric='mae',
    n_individuals=500,
    n_generations=100,
    random_state=42,
    parsimony_coefficient=0.01
)

model.fit(X, y, verbose=True)

print('MAE: {:.5f}'.format(metrics.mean_absolute_error(y, model.predict(X))))
