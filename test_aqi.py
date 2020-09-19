from aqi import aqi25
def test_sample():
    assert (aqi25(10) == 81), "should yield 81"