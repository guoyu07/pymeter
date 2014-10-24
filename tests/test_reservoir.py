from pymeter.reservoir import ExponentiallyDecayingReservoir
from .util import ManualClock


def assert_all_values_between(reservoir, min_value, max_value):
    for value in reservoir.snapshot().values:
        assert min_value <= value < max_value


def test_a_reservoir_of_100_out_of_1000_elements():
    reservoir = ExponentiallyDecayingReservoir(100, 0.99)
    for i in xrange(1000):
        reservoir.update(i)
    assert len(reservoir) == 100
    snapshot = reservoir.snapshot()
    assert len(snapshot) == 100
    assert_all_values_between(reservoir, 0, 1000)


def test_a_reservoir_of_100_out_of_10_elements():
    reservoir = ExponentiallyDecayingReservoir(100, 0.99)
    for i in xrange(10):
        reservoir.update(i)
    assert len(reservoir) == 10
    snapshot = reservoir.snapshot()
    assert len(snapshot) == 10
    assert_all_values_between(reservoir, 0, 10)


def test_a_heavily_biased_reservoir_of_100_out_of_1000_elements():
    reservoir = ExponentiallyDecayingReservoir(1000, 0.01)
    for i in xrange(100):
        reservoir.update(i)
    assert len(reservoir) == 100
    snapshot = reservoir.snapshot()
    assert len(snapshot) == 100
    assert_all_values_between(reservoir, 0, 100)


def test_long_period_of_inactivity_should_not_corrupt_sampling_state():
    clock = ManualClock()
    reservoir = ExponentiallyDecayingReservoir(10, 0.015, clock)

    # add 1000 values at a rate of 10 values / second
    for i in xrange(1000):
        reservoir.update(1000 + i)
        clock.add_millis(100)

    assert len(reservoir.snapshot()) == 10
    assert_all_values_between(reservoir, 1000, 2000)

    # wait for 15 hours and add another value.
    # this should trigger a rescale. Note that the number of samples will be reduced to 2
    # because of the very small scaling factor that will make all existing priorities equal to zero after rescale.
    clock.add_hours(15)
    reservoir.update(2000)
    assert len(reservoir.snapshot()) == 2
    assert_all_values_between(reservoir, 1000, 3000)

    # add 1000 values at a rate of 10 values / second
    for i in xrange(1000):
        reservoir.update(3000 + i)
        clock.add_millis(100)

    assert len(reservoir.snapshot()) == 10
    assert_all_values_between(reservoir, 3000, 4000)


def test_spot_lift():
    clock = ManualClock()
    reservoir = ExponentiallyDecayingReservoir(1000, 0.015, clock)
    rate_per_minute = 10
    interval_millis = 60 * 1000 / rate_per_minute

    # mode 1: steady regime for 120 minutes
    for i in xrange(120 * rate_per_minute):
        reservoir.update(177)
        clock.add_millis(interval_millis)

    # switching to mode 2: 10 more minutes with the same rate, but larger value
    for i in xrange(10 * rate_per_minute):
        reservoir.update(9999)
        clock.add_millis(interval_millis)

    # expect that quantiles should be more about mode 2 after 10 minutes
    assert reservoir.snapshot().median == 9999


def test_spot_fall():
    clock = ManualClock()
    reservoir = ExponentiallyDecayingReservoir(1000, 0.015, clock)
    rate_per_minute = 10
    interval_millis = 60 * 1000 / rate_per_minute

    # mode 1: steady regime for 120 minutes
    for i in xrange(120 * rate_per_minute):
        reservoir.update(9998)
        clock.add_millis(interval_millis)

    # switching to mode 2: 10 more minutes with the same rate, but smaller value
    for i in xrange(10 * rate_per_minute):
        reservoir.update(178)
        clock.add_millis(interval_millis)

    # expect that quantiles should be more about mode 2 after 10 minutes
    print reservoir.snapshot().p95
    assert reservoir.snapshot().p95 == 178


def test_quantiles_should_be_based_on_weights():
    clock = ManualClock()
    reservoir = ExponentiallyDecayingReservoir(1000, 0.015, clock)

    for i in xrange(40):
        reservoir.update(177)
    clock.add_seconds(120)
    for i in xrange(10):
        reservoir.update(9999)

    assert len(reservoir.snapshot()) == 50

    # the first added 40 items (177) have weights 1
    # the next added 10 items (9999) have weights ~6
    # so, it's 40 vs 60 distribution, not 40 vs 10
    assert reservoir.snapshot().median == 9999
    assert reservoir.snapshot().p75 == 9999
