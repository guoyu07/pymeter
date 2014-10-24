from pymeter.ewma import EWMA
from util import close_enough

__author__ = 'binhle'


def elapse_one_minute(ewma):
    for i in xrange(12):
        ewma.tick()


def test_one_minute_ewma_with_a_value_of_three():
    ewma = EWMA.one_minute_ewma()
    ewma.update(3)

    ewma.tick()
    assert close_enough(ewma.rate, 0.6, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.22072766, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.08120117, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.02987224, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.01098938, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.00404277, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.00148725, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.00054713, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.00020128, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.00007405, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.00002724, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.00001002, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.00000369, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.00000136, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.00000050, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.00000018, offset=0.000001)


def test_five_minute_ewma_with_a_value_of_three():
    ewma = EWMA.five_minute_ewma()
    ewma.update(3)

    ewma.tick()
    assert close_enough(ewma.rate, 0.6, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.49123845, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.40219203, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.32928698, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.26959738, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.22072766, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.18071653, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.14795818, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.12113791, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.09917933, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.08120117, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.06648190, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.05443077, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.04456415, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.03648604, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.02987224, offset=0.000001)


def test_fifteen_minute_ewma_with_a_value_of_three():
    ewma = EWMA.fifteen_minute_ewma()
    ewma.update(3)

    ewma.tick()
    assert close_enough(ewma.rate, 0.6, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.56130419, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.52510399, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.49123845, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.45955700, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.42991879, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.40219203, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.37625345, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.35198773, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.32928698, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.30805027, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.28818318, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.26959738, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.25221023, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.23594443, offset=0.000001)

    elapse_one_minute(ewma)
    assert close_enough(ewma.rate, 0.22072766, offset=0.000001)
