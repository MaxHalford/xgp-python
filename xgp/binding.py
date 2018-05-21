import ctypes
import glob
import os
import numpy as np


def find_xgp_dll_paths():
    """Finds the XGP dynamic library file."""
    here = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))

    def make_paths(ext):
        return [
            *glob.glob(os.path.join(here, 'xgp*.{}'.format(ext))),
            *glob.glob(os.path.join(here, '..', 'xgp*.{}'.format(ext))),
            *glob.glob(os.path.join(here, '../..', 'xgp*.{}'.format(ext))),
        ]

    return make_paths('so') + make_paths('dll') + make_paths('pyd')


def load_dll(path):
    """Loads and returns a dynamic library file."""
    return ctypes.cdll.LoadLibrary(path)


class GoString(ctypes.Structure):
    _fields_ = [
        ('p', ctypes.c_char_p),
        ('n', ctypes.c_longlong)
    ]


class GoFloat64Slice(ctypes.Structure):
    _fields_ = [
        ('data', ctypes.POINTER(ctypes.c_double)),
        ('len', ctypes.c_longlong),
        ('cap', ctypes.c_longlong)
    ]


class GoFloat64Matrix(ctypes.Structure):
    _fields_ = [
        ('data', ctypes.POINTER(GoFloat64Slice)),
        ('len', ctypes.c_longlong),
        ('cap', ctypes.c_longlong)
    ]


def numpy_to_slice(arr: np.ndarray) -> GoFloat64Slice:
    # If the slice is 1D then return a GoFloat64Slice
    if len(arr.shape) == 1:
        return GoFloat64Slice(
            arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            len(arr),
            len(arr)
        )
    # If not return a GoFloat64Matrix composed of GoFloat64Slices
    return GoFloat64Matrix(
        (GoFloat64Slice * len(arr))(*[
            numpy_to_slice(arr[i, :])
            for i in range(len(arr))
        ]),
        len(arr),
        len(arr)
    )


def str_to_go_string(s: str):
    return GoString(bytes(s, 'utf-8'), len(s))


def fit(X_train: np.ndarray,
        y_train: np.ndarray,
        w_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        w_val: np.ndarray,

        loss_metric_name: str,
        eval_metric_name: str,
        parsimony_coefficient: float,

        funcs: str,
        const_min: float,
        const_max: float,
        p_constant: float,
        p_full: float,
        p_terminal: float,
        min_height: int,
        max_height: int,

        n_populations: int,
        n_individuals: int,
        n_generations: int,
        n_polish_generations: int,
        p_hoist_mutation: float,
        p_sub_tree_mutation: float,
        p_point_mutation: float,
        point_mutation_rate: float,
        p_sub_tree_crossover: float,

        seed: int,
        verbose: bool):
    """Refers to the Fit method in main.go"""

    # Find the and load the XGP dynamic library file
    paths = find_xgp_dll_paths()
    if len(paths) == 0:
        raise RuntimeError("Can't find any XGP dynamic library files")
    lib = load_dll(paths[0])

    # Use Fortran memory layout (and not contiguous memory layout)
    X_train = np.asfortranarray(X_train.astype(float))
    y_train = np.asfortranarray(y_train.astype(float))
    if w_train is not None:
        w_train = np.asfortranarray(w_train.astype(float))
    if X_val is not None:
        X_val = np.asfortranarray(X_val.astype(float))
    if y_val is not None:
        y_val = np.asfortranarray(y_val.astype(float))
    if X_val is not None:
        X_val = np.asfortranarray(X_val.astype(float))

    args = [
        (numpy_to_slice(X_train.T), GoFloat64Matrix),
        (numpy_to_slice(y_train), GoFloat64Slice),
        (numpy_to_slice(w_train if w_train is not None else np.zeros(shape=0)), GoFloat64Slice),
        (numpy_to_slice(X_val.T if X_val is not None else np.zeros(shape=(0, 0))), GoFloat64Matrix),
        (numpy_to_slice(y_val if y_val is not None else np.zeros(shape=0)), GoFloat64Slice),
        (numpy_to_slice(w_val if w_val is not None else np.zeros(shape=0)), GoFloat64Slice),

        (str_to_go_string(loss_metric_name), GoString),
        (str_to_go_string(eval_metric_name if eval_metric_name else ''), GoString),
        (parsimony_coefficient, ctypes.c_double),

        (str_to_go_string(funcs), GoString),
        (const_min, ctypes.c_double),
        (const_max, ctypes.c_double),
        (p_constant, ctypes.c_double),
        (p_full, ctypes.c_double),
        (p_terminal, ctypes.c_double),
        (min_height, ctypes.c_longlong),
        (max_height, ctypes.c_longlong),

        (n_populations, ctypes.c_longlong),
        (n_individuals, ctypes.c_longlong),
        (n_generations, ctypes.c_longlong),
        (n_polish_generations, ctypes.c_longlong),
        (p_hoist_mutation, ctypes.c_double),
        (p_sub_tree_mutation, ctypes.c_double),
        (p_point_mutation, ctypes.c_double),
        (point_mutation_rate, ctypes.c_double),
        (p_sub_tree_crossover, ctypes.c_double),

        (seed, ctypes.c_longlong),
        (verbose, ctypes.c_bool)
    ]

    lib.Fit.argtypes = [arg[1] for arg in args]
    lib.Fit.restype = ctypes.c_char_p

    return lib.Fit(*[arg[0] for arg in args])
