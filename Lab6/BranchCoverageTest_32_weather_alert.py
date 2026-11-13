import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

def test_wind_alert_all_branches():
    assert wind_alert(89) == "warning"
    assert wind_alert(62) == "watch"
    assert wind_alert(39) == "advisory"
    assert wind_alert(38) == "none"

def test_rain_alert_all_branches():
    assert rain_alert(50, True) == "warning"
    assert rain_alert(50, False) == "watch"
    assert rain_alert(10, True) == "watch"
    assert rain_alert(10, False) == "advisory"
    assert rain_alert(9, True) == "none"

def test_heat_alert_all_branches():
    assert heat_alert(43, 60) == "warning"   
    assert heat_alert(40, 40) == "watch"     
    assert heat_alert(35, 30) == "advisory"  
    assert heat_alert(34, 20) == "none"      

def test_overall_alert_all_branches():
    assert overall_alert([]) == "none"
    assert overall_alert(["watch", "advisory", "warning", "none"]) == "warning"
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["advisory", "unknown"])