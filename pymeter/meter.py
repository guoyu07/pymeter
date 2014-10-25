import time
import functools

from .ewma import EWMA, INTERVAL


class Meter(object):
    """
    A meter that measures mean throughput and one-, five-, fifteen-minute
    exponentially-weighted moving average throughput.

    All reported rates are measured as event per second.
    """

    def __init__(self, clock=time):
        self.clock = clock
        self.start_time = clock.time()
        self.last_tick = self.start_time
        self.count = 0
        self._m1_rate = EWMA.one_minute_ewma()
        self._m5_rate = EWMA.five_minute_ewma()
        self._m15_rate = EWMA.fifteen_minute_ewma()

    def mark(self, n=1):
        """
        Mark the occurrence of a given number of events.

        :param n: the number of events
        """
        self._tick_if_needed()
        self.count += n
        self._m1_rate.update(n)
        self._m5_rate.update(n)
        self._m15_rate.update(n)

    def _tick_if_needed(self):
        new_tick = self.clock.time()
        age = new_tick - self.last_tick
        if age > INTERVAL:
            self.last_tick = new_tick - age % INTERVAL
            required_ticks = int(age / INTERVAL)
            for i in xrange(required_ticks):
                self._m1_rate.tick()
                self._m5_rate.tick()
                self._m15_rate.tick()

    @property
    def mean_rate(self):
        """
        :return: mean rate at which events had occurred since the meter was created.
        """
        if self.count == 0:
            return 0.0
        elapsed = self.clock.time() - self.start_time
        return self.count / elapsed

    @property
    def one_minute_rate(self):
        """
        :return: one-minute exponentially-weighted moving average rate at which events have occurred
        since the meter was created.
        """
        return self._m1_rate.rate

    @property
    def five_minute_rate(self):
        """
        :return: five-minute exponentially-weighted moving average rate at which events have occurred
        since the meter was created.
        """
        return self._m5_rate.rate

    @property
    def fifteen_minute_rate(self):
        """
        :return: fifteen-minute exponentially-weighted moving average rate at which events have occurred
        since the meter was created.
        """
        return self._m15_rate.rate


def metered(clock=time):
    def decorator(func):
        meter = Meter(clock=clock)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            meter.mark()
            return func(*args, **kwargs)

        wrapper.meter = meter
        return wrapper

    return decorator

