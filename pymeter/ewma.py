from __future__ import division
import math


INTERVAL = 5
M1_ALPHA = 1 - math.exp(-INTERVAL / 60 / 1)
M5_ALPHA = 1 - math.exp(-INTERVAL / 60 / 5)
M15_ALPHA = 1 - math.exp(-INTERVAL / 60 / 15)


class EWMA(object):
    """
    An exponentially-weighted moving average
    """

    def __init__(self, alpha, interval):
        self.alpha = alpha
        self.interval = interval
        self.rate = 0.0
        self._uncounted = 0
        self._initialized = False

    @classmethod
    def one_minute_ewma(cls):
        return cls(M1_ALPHA, INTERVAL)

    @classmethod
    def five_minute_ewma(cls):
        return cls(M5_ALPHA, INTERVAL)

    @classmethod
    def fifteen_minute_ewma(cls):
        return cls(M15_ALPHA, INTERVAL)

    def update(self, n):
        self._uncounted += n

    def tick(self):
        instance_rate = self._uncounted / self.interval
        self._uncounted = 0
        if self._initialized:
            self.rate += self.alpha * (instance_rate - self.rate)
        else:
            self.rate = instance_rate
            self._initialized = True
