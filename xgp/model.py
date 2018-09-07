import abc
import json

import numpy as np
from sklearn import base
from sklearn import utils

from . import binding
from . import parse


class XGPModel(abc.ABC, base.BaseEstimator):
    """ Implementation of the scikit-learn API for XGP.

    Parameters
    ----------
    flavor : str
        Indicates what kind of algoritm to perform. The possible values are:
            - 'vanilla': plain genetic programming
            - 'boosting': gradient boosting on top of genetic programming
    loss_metric : str
        Metric used for scoring program; determines the task to perform.
    parsimony_coefficient : float
        Parsimony coefficient by which a program's height is multiplied to
        penalize it's fitness.
    polish_best : bool
        Whether or not to polish the best program.
    funcs : str
        Comma-separated set of authorised functions.
    const_min : float
        Lower bound used for generating constants.
    const_max : float
        Upper bound used for generating constants.
    p_const : float
        Probability of generating a constant instead of a variable.
    p_full : float
        Probability of using full initialization during ramped half-and-half
        initialization.
    p_leaf : float
        Probability of generating a terminal node during ramped half-and-half
        initialization.
    min_height : int
        Minimum program height used in ramped half-and-half initialization.
    max_height : int
        Minimum program height used in ramped half-and-half initialization.
    n_populations : int
        Number of populations used in the genetic algorithm.
    n_individuals : int
        Number of individuals used for each population in the genetic
        algorithm.
    n_generations : int
        Number of generations used in the GA.
    p_hoist_mutation : float
        Probability of applying hoist mutation.
    p_sub_tree_mutation : float
        Probability of applying subtree mutation.
    p_point_mutation : float
        Probability of applying point mutation.
    point_mutation_rate : float
        Probability of modifying an operator during point mutation.
    p_sub_tree_crossover : float
        Probability of applying subtree crossover.
    n_rounds : int
        Number of rounds to use in case of an ensemble model.
    n_early_stopping_rounds : int
        Number of rounds used when motinoring early stopping.
    learning_rate : float
        Learning rate used for gradient boosting.
    line_search : bool
        Whether or not to use line search for gradient boosting.
    random_state : int, RandomState instance or None, optional (default=None)
        Control the randomization of the algorithm

        - If int, ``random_state`` is the seed used by the random number
          generator;
        - If ``RandomState`` instance, random_state is the random number
          generator;
        - If ``None``, the random number generator is the ``RandomState``
          instance used by ``np.random``.

    Attributes
    ----------
    program_json_ : dict
        The JSON representation of the best program.
    """

    @property
    @abc.abstractmethod
    def default_loss(self):
        raise ValueError('No default loss has been specified, please specify one')

    def __init__(self, flavor='boosting', loss_metric='', parsimony_coefficient=0.00001,
                 polish_best=True, funcs='add,sub,mul,div', const_min=-5, const_max=5, p_const=0.5,
                 p_full=0.5, p_leaf=0.3, min_height=3, max_height=5, n_populations=1,
                 n_individuals=100, n_generations=30, p_hoist_mutation=0.1, p_sub_tree_mutation=0.1,
                 p_point_mutation=0.1, point_mutation_rate=0.5, p_sub_tree_crossover=0.3,
                 n_rounds=50, n_early_stopping_rounds=5, learning_rate=0.08, line_search=True,
                 random_state=None):


        self.flavor = flavor

        # GP parameters
        self.loss_metric = loss_metric if loss_metric else self.default_loss
        self.parsimony_coefficient = parsimony_coefficient
        self.polish_best = polish_best
        self.funcs = funcs
        self.const_min = const_min
        self.const_max = const_max
        self.p_hoist_mutation = p_hoist_mutation
        self.p_sub_tree_mutation = p_sub_tree_mutation
        self.p_point_mutation = p_point_mutation
        self.point_mutation_rate = point_mutation_rate
        self.min_height = min_height
        self.max_height = max_height

        # GA parameters
        self.n_populations = n_populations
        self.n_individuals = n_individuals
        self.n_generations = n_generations
        self.p_const = p_const
        self.p_full = p_full
        self.p_leaf = p_leaf
        self.p_sub_tree_crossover = p_sub_tree_crossover

        # Ensemble parameters
        self.n_rounds = n_rounds
        self.n_early_stopping_rounds = n_early_stopping_rounds
        self.learning_rate = learning_rate
        self.line_search = line_search

        # Other
        self.random_state = random_state

    def fit(self, X, y, sample_weight=None, eval_set=None, eval_metric=None,
            eval_sample_weight=None, verbose=False):

        X, y = utils.check_X_y(X, y)
        if sample_weight is not None:
            sample_weight = utils.check_array(sample_weight, ensure_2d=False)
        if eval_sample_weight is not None:
            eval_sample_weight = utils.check_array(eval_sample_weight, ensure_2d=False)

        # Extract the validation set
        X_val = None
        y_val = None
        if eval_set is not None:
            X_val = eval_set[0]
            y_val = eval_set[1]
            X_val, y_val = utils.check_X_y(X_val, y_val)

        program_raw_json = binding.fit(
            X_train=X,
            y_train=y,
            w_train=sample_weight,
            X_val=X_val,
            y_val=y_val,
            w_val=eval_sample_weight,

            flavor=self.flavor,

            # GP parameters
            loss_metric_name=self.loss_metric,
            eval_metric_name=eval_metric,
            parsimony_coefficient=self.parsimony_coefficient,
            polish_best=self.polish_best,
            funcs=self.funcs,
            const_min=self.const_min,
            const_max=self.const_max,
            p_const=self.p_const,
            p_full=self.p_full,
            p_leaf=self.p_leaf,
            min_height=self.min_height,
            max_height=self.max_height,

            # GA parameters
            n_populations=self.n_populations,
            n_individuals=self.n_individuals,
            n_generations=self.n_generations,
            p_hoist_mutation=self.p_hoist_mutation,
            p_sub_tree_mutation=self.p_sub_tree_mutation,
            p_point_mutation=self.p_point_mutation,
            point_mutation_rate=self.point_mutation_rate,
            p_sub_tree_crossover=self.p_sub_tree_crossover,

            # Ensemble parameters
            n_rounds=self.n_rounds,
            n_early_stopping_rounds=self.n_early_stopping_rounds,
            learning_rate=self.learning_rate,
            line_search=self.line_search,

            # Other
            seed=utils.check_random_state(self.random_state).randint(2 ** 24),
            verbose=verbose
        )

        self.model_json_ = json.loads(program_raw_json.decode('utf-8'))

        return self

    def predict(self, X):
        utils.validation.check_is_fitted(self, 'model_json_')
        X = utils.check_array(X)

        if self.flavor == 'vanilla':
            return parse.parse_program_json(self.model_json_['op'])(X)

        if self.flavor == 'boosting':
            y_pred = np.full(shape=len(X), fill_value=self.model_json_['y_mean'])
            for prog, step in zip(map(lambda prog: parse.parse_program_json(prog['op']), self.model_json_['programs']), self.model_json_['steps']):
                update = prog(X)
                y_pred = y_pred - self.learning_rate * step * update
            return y_pred

        raise ValueError('Unknown flavor')
