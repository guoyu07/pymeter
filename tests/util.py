from __future__ import division


def close_enough(actual, expected, offset=0.001):
    return abs(actual - expected) <= offset


class ManualClock(object):
    def __init__(self):
        self._time = 0.0

    def add_millis(self, millis):
        self._time += millis / 1000

    def add_seconds(self, seconds):
        self._time += seconds

    def add_hours(self, hours):
        self._time += hours * 3600

    def time(self):
        return self._time
