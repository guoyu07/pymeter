import time
import functools

from pymeter.reservoir import ExponentiallyDecayingReservoir
from pymeter.meter import Meter
from pymeter.histogram import Histogram


class TimedContext(object):
    def __init__(self, timer, clock):
        self.timer = timer
        self.clock = clock
        self.start_time = None

    def __enter__(self):
        self.start_time = self.clock.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = self.clock.time() - self.start_time
        self.timer.update(elapsed)


class Timer(object):
    def __init__(self, reservoir=None, clock=time):
        self.reservoir = reservoir if reservoir is not None else ExponentiallyDecayingReservoir()
        self.histogram = Histogram(self.reservoir)
        self.clock = clock
        self.meter = Meter(clock)

    def update(self, duration):
        """
        Add a recorded duration.

        :param duration: the length of the duration
        """
        if duration >= 0:
            self.meter.mark()
            self.histogram.update(duration)

    def time(self, func):
        """
        Call a function, record and time its durations.

        :param func: the function to be called and timed
        """
        start_time = self.clock.time()
        try:
            return func()
        finally:
            self.update(self.clock.time() - start_time)

    def timed_context(self):
        return TimedContext(self, self.clock)

    @property
    def count(self):
        return self.histogram.count

    @property
    def mean_rate(self):
        return self.meter.mean_rate

    @property
    def one_minute_rate(self):
        return self.meter.one_minute_rate

    @property
    def five_minute_rate(self):
        return self.meter.five_minute_rate

    @property
    def fifteen_minute_rate(self):
        return self.meter.five_minute_rate

    def snapshot(self):
        return self.histogram.snapshot()


def timed(reservoir=None, clock=None):
    def decorator(func):
        timer = Timer(reservoir=reservoir, clock=clock)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with timer.timed_context():
                return func(*args, **kwargs)

        wrapper.timer = timer
        return wrapper

    return decorator
