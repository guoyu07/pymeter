from pymeter.meter import Meter, metered
from util import ManualClock, close_enough


def test_starts_out_with_no_rates_or_count():
    meter = Meter()
    assert meter.count == 0
    assert close_enough(meter.mean_rate, 0)
    assert close_enough(meter.one_minute_rate, 0)
    assert close_enough(meter.five_minute_rate, 0)
    assert close_enough(meter.fifteen_minute_rate, 0)


def test_meter():
    clock = ManualClock()
    meter = Meter(clock)
    meter.mark()
    clock.add_seconds(10)
    meter.mark(2)

    assert close_enough(meter.mean_rate, 0.3)
    assert close_enough(meter.one_minute_rate, 0.1840)
    assert close_enough(meter.five_minute_rate, 0.1966)
    assert close_enough(meter.fifteen_minute_rate, 0.1988)


def test_decorator():
    clock = ManualClock()

    @metered(clock=clock)
    def foo():
        pass

    for i in xrange(10):
        foo()
        clock.add_seconds(10)

    assert close_enough(foo.meter.mean_rate, 0.1)
    assert close_enough(foo.meter.one_minute_rate, 0.119)
    assert close_enough(foo.meter.five_minute_rate, 0.174)
    assert close_enough(foo.meter.fifteen_minute_rate, 0.190)
