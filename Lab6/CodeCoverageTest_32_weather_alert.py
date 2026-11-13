import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

def test_wind_alert():
    assert wind_alert(95) == "warning"
    assert wind_alert(70) == "watch"
    assert wind_alert(45) == "advisory"
    assert wind_alert(10) == "none"

def test_rain_alert():
    assert rain_alert(60, True) == "warning"
    assert rain_alert(60, False) == "watch"
    assert rain_alert(20, True) == "watch"
    assert rain_alert(20, False) == "advisory"
    assert rain_alert(5, False) == "none"

def test_heat_alert():
    assert heat_alert(44, 60) == "warning"
    assert heat_alert(39, 60) == "watch"
    assert heat_alert(34, 60) == "advisory"
    assert heat_alert(25, 60) == "none"

def test_overall_alert():
    assert overall_alert([]) == "none"
    assert overall_alert(["advisory", "warning"]) == "warning"
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["invalid_alert"])