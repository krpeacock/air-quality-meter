from aqi import aqi
def test_sample():
    assert (aqi(10) == 81), "should yield 81"