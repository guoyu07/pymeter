import time
import random
import math

from pymeter.snapshot import WeightedSample, WeightedSnapshot


__author__ = 'binhle'


class ExponentiallyDecayingReservoir(object):
    rescale_threshold = 3600

    def __init__(self, size=1028, alpha=0.015, clock=time):
        self.values = {}
        self.size = size
        self.alpha = alpha
        self.count = 0
        self.clock = clock
        self._start_time = self.clock.time()
        self._next_scale_time = self._start_time + self.rescale_threshold

    def __len__(self):
        return min(self.size, self.count)

    def update(self, value, timestamp=None):
        self._rescale_if_needed()
        if timestamp is None:
            timestamp = self.clock.time()
        weight = self._weight(timestamp - self._start_time)
        sample = WeightedSample(value, weight)
        priority = weight / random.random()
        self.count += 1
        if self.count <= self.size:
            self.values[priority] = sample
        else:
            lowest = min(self.values)
            if lowest < priority and priority not in self.values:
                self.values[priority] = sample
                del self.values[lowest]

    def snapshot(self):
        return WeightedSnapshot(self.values.itervalues())

    def _rescale_if_needed(self):
        now = self.clock.time()
        if now >= self._next_scale_time:
            self._rescale(now, self._next_scale_time)

    def _rescale(self, now, next):
        self._next_scale_time = now + self.rescale_threshold
        old_start_time = self._start_time
        self._start_time = start_time = self.clock.time()
        scaling_factor = math.exp(-self.alpha * (start_time - old_start_time))
        for key in self.values.keys():
            sample = self.values.pop(key)
            scaled_sample = WeightedSample(sample.value, sample.weight * scaling_factor)
            self.values[key * scaling_factor] = scaled_sample

        # make sure the counter is in sync with the number of stored samples
        self.count = len(self.values)

    def _weight(self, t):
        return math.exp(self.alpha * t)

