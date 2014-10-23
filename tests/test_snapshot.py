from nose.tools import raises

from pymeter.snapshot import WeightedSample, WeightedSnapshot
from .util import close_enough


__author__ = 'binhle'


def weighted_array(values, weights):
    return (WeightedSample(v, w) for v, w in zip(values, weights))


snapshot = WeightedSnapshot(weighted_array([5, 1, 2, 3, 4], [1, 2, 3, 2, 2]))
empty_snapshot = WeightedSnapshot([])


def test_small_quantiles_are_the_first_value():
    assert close_enough(snapshot.get_value(0), 1)


def test_big_quantiles_are_the_last_value():
    assert close_enough(snapshot.get_value(1), 5)


@raises(ValueError)
def test_nan_quantile():
    snapshot.get_value(float('nan'))


@raises(ValueError)
def test_negative_quantile():
    snapshot.get_value(-0.5)


@raises(ValueError)
def test_larger_than_one_quantile():
    snapshot.get_value(1.5)


def test_median():
    assert close_enough(snapshot.median, 3)


def test_p75():
    assert close_enough(snapshot.p75, 4)


def test_p95():
    assert close_enough(snapshot.p95, 5)


def test_p98():
    assert close_enough(snapshot.p98, 5)


def test_p99():
    assert close_enough(snapshot.p99, 5)


def test_p999():
    assert close_enough(snapshot.p999, 5)


def test_values():
    assert set(snapshot.values) == {1, 2, 3, 4, 5}


def test_len():
    assert len(snapshot) == 5


def test_min():
    assert snapshot.min == 1


def test_max():
    assert snapshot.max == 5


def test_mean():
    assert snapshot.mean == 2.7


def test_std_dev():
    print snapshot.std_dev
    assert close_enough(snapshot.std_dev, 1.2688, offset=0.0001)


def test_empty_snapshot():
    assert empty_snapshot.min == 0
    assert empty_snapshot.max == 0
    assert empty_snapshot.mean == 0
    assert empty_snapshot.std_dev == 0


def test_std_dev_of_singleton_snapshot_is_zero():
    single_item_snapshot = WeightedSnapshot([WeightedSample(1, 1)])
    assert single_item_snapshot.std_dev == 0

