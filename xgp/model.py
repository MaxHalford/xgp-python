import abc

from sklearn import base
from sklearn import utils

from . import binding
from . import parse


class XGPModel(abc.ABC, base.BaseEstimator):
    """ Implementation of the scikit-learn API for XGP.

    Parameters
    ----------
    loss_metric : str
        Metric used for scoring program; determines the task to perform.
    parsimony_coefficient : float
        Parsimony coefficient by which a program's height is multiplied to
        penalize it's fitness.
    funcs : str
        Comma-separated set of authorised functions.
    const_min : float
        Lower bound used for generating constants.
    const_max : float
        Upper bound used for generating constants.
    p_constant : float
        Probability of generating a constant instead of a variable.
    p_full : float
        Probability of using full initialization during ramped half-and-half
        initialization.
    p_terminal : float
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
    n_polish_generations : int
        Number of generations used to polish the best program.
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
    program_str_ : str
        The string representation of the best program.
    """

    @property
    @abc.abstractmethod
    def default_loss(self):
        pass

    def __init__(self, loss_metric='', parsimony_coefficient=0.00001,
                 funcs='sum,sub,mul,div', const_min=-5, const_max=5,
                 p_constant=0.5, p_full=0.5, p_terminal=0.3, min_height=3,
                 max_height=5, n_populations=1, n_individuals=100,
                 n_generations=30, n_polish_generations=0,
                 p_hoist_mutation=0.1, p_sub_tree_mutation=0.1,
                 p_point_mutation=0.1, point_mutation_rate=0.5,
                 p_sub_tree_crossover=0.3, random_state=None):

        self.loss_metric = loss_metric
        self.parsimony_coefficient = parsimony_coefficient

        self.funcs = funcs
        self.const_min = const_min
        self.const_max = const_max
        self.p_hoist_mutation = p_hoist_mutation
        self.p_sub_tree_mutation = p_sub_tree_mutation
        self.p_point_mutation = p_point_mutation
        self.point_mutation_rate = point_mutation_rate
        self.min_height = min_height
        self.max_height = max_height

        self.n_populations = n_populations
        self.n_individuals = n_individuals
        self.n_generations = n_generations
        self.n_polish_generations = n_polish_generations
        self.p_constant = p_constant
        self.p_full = p_full
        self.p_terminal = p_terminal
        self.p_sub_tree_crossover = p_sub_tree_crossover

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

        program_bytes_ = binding.fit(
            X_train=X,
            y_train=y,
            w_train=sample_weight,
            X_val=X_val,
            y_val=y_val,
            w_val=eval_sample_weight,

            loss_metric_name=self.loss_metric if self.loss_metric else self.default_loss,
            eval_metric_name=eval_metric,
            parsimony_coefficient=self.parsimony_coefficient,

            funcs=self.funcs,
            const_min=self.const_min,
            const_max=self.const_max,
            p_constant=self.p_constant,
            p_full=self.p_full,
            p_terminal=self.p_terminal,
            min_height=self.min_height,
            max_height=self.max_height,

            n_populations=self.n_populations,
            n_individuals=self.n_individuals,
            n_generations=self.n_generations,
            n_polish_generations=self.n_polish_generations,
            p_hoist_mutation=self.p_hoist_mutation,
            p_sub_tree_mutation=self.p_sub_tree_mutation,
            p_point_mutation=self.p_point_mutation,
            point_mutation_rate=self.point_mutation_rate,
            p_sub_tree_crossover=self.p_sub_tree_crossover,

            seed=utils.check_random_state(self.random_state).randint(2 ** 24),
            verbose=verbose
        )

        self.program_str_ = program_bytes_.decode('utf-8')

        return self

    def predict(self, X):
        utils.validation.check_is_fitted(self, 'program_str_')
        X = utils.check_array(X)
        return parse.parse_code(self.program_str_)(X)
