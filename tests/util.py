__author__ = 'binhle'


def close_enough(actual, expected, offset=0.1):
    return abs(actual - expected) <= offset
