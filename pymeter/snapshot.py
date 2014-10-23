from __future__ import division
from bisect import bisect_left
from collections import namedtuple
import math
import abc


__author__ = 'binhle'


class Snapshot(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_value(self, param):
        pass

    @property
    def median(self):
        return self.get_value(0.5)

    @property
    def p75(self):
        return self.get_value(0.75)

    @property
    def p95(self):
        return self.get_value(0.95)

    @property
    def p98(self):
        return self.get_value(0.98)

    @property
    def p99(self):
        return self.get_value(0.99)

    @property
    def p999(self):
        return self.get_value(0.999)


WeightedSample = namedtuple('WeightedSample', ['value', 'weight'])


class WeightedSnapshot(Snapshot):
    def __init__(self, samples):
        copy = sorted(samples, key=lambda s: s.value)
        sum_weight = sum(s.weight for s in copy)

        self.values = []
        self.norm_weights = []
        for sample in copy:
            self.values.append(sample.value)
            self.norm_weights.append(sample.weight / sum_weight)

        self.quantiles = [0]
        for i in xrange(1, len(copy)):
            self.quantiles.append(self.quantiles[i - 1] + self.norm_weights[i - 1])

    def get_value(self, quantile):
        """
        Return the value at the given quantile.

        :param quantile: a given quantile
        :return: the value in the distribution at given quantile
        """
        if quantile < 0 or quantile > 1 or math.isnan(quantile):
            raise ValueError

        if not self.values:
            return 0.0

        pos = bisect_left(self.quantiles, quantile)
        if pos >= len(self.quantiles) or self.quantiles[pos] != quantile:
            pos -= 1

        if pos < 1:
            return self.values[0]

        if pos >= len(self.values):
            return self.values[-1]

        return self.values[pos]

    def __len__(self):
        return len(self.values)

    @property
    def max(self):
        return self.values[-1] if self.values else 0

    @property
    def min(self):
        return self.values[0] if self.values else 0

    @property
    def mean(self):
        return sum(v * w for v, w in zip(self.values, self.norm_weights)) if self.values else 0

    @property
    def std_dev(self):
        if len(self.values) <= 1:
            return 0
        mean = self.mean
        diffs = (value - mean for value in self.values)
        variance = sum(diff * diff * weight for diff, weight in zip(diffs, self.norm_weights))
        return math.sqrt(variance)
