class Histogram(object):
    """
    A metric which calculates the distribution of a value.
    """

    def __init__(self, reservoir):
        """
        Create a new histogram with given reservoir.

        :param reservoir: the reservoir used to create histogram from
        """
        self.reservoir = reservoir
        self.count = 0

    def update(self, value):
        """
        Add a recorded value.

        :param value: the recorded value
        """
        self.count += 1
        self.reservoir.update(value)

    def snapshot(self):
        """
        Return a snapshot of the values in this histogram.
        """
        return self.reservoir.snapshot()
