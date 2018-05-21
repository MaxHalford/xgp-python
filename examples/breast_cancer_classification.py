from sklearn import datasets
from sklearn import metrics
from sklearn import model_selection
import xgp


X, y = datasets.load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, random_state=42)

model = xgp.XGPClassifier(
    loss_metric='logloss',
    n_individuals=500,
    n_generations=100,
    random_state=42,
    parsimony_coefficient=0.01
)

model.fit(X_train, y_train, eval_set=(X_test, y_test), verbose=True)

print('Train F1: {:.5f}'.format(metrics.f1_score(y_train, model.predict(X_train))))
print('Test F1: {:.5f}'.format(metrics.f1_score(y_test, model.predict(X_test))))

print('Train log-loss: {:.5f}'.format(metrics.log_loss(y_train, model.predict_proba(X_train))))
print('Test log-loss: {:.5f}'.format(metrics.log_loss(y_test, model.predict_proba(X_test))))
