import numpy as np

from xgp import binding


def test_numpy_to_slice():
    """Test numpy_to_slice"""
    X = np.array([
        [11, 12, 13],
        [21, 22, 23]
    ])
    go_slice = binding.numpy_to_slice(X)
    assert isinstance(go_slice, binding.GoFloat64Matrix)
    assert go_slice.len == 2
    assert go_slice.cap == 2
    assert go_slice.data[0].len == 3
    assert go_slice.data[0].cap == 3
    assert go_slice.data[1].len == 3
    assert go_slice.data[1].cap == 3
