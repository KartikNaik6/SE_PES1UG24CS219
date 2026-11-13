from hypothesis import given, strategies as st
from weather_alert import parse_reading, wind_category, rainfall_spread

@given(st.text() | st.none())
def test_parse_reading_no_crash(s):
    try:
        parse_reading(s)
    except (ValueError, TypeError, AttributeError):
        pass

@given(st.text() | st.none())
def test_wind_category_no_crash(s):
    try:
        wind_category(s)
    except (ValueError, TypeError):
        pass

@given(st.text() | st.none())
def test_rainfall_spread_no_crash(s):
    try:
        rainfall_spread(s)
    except (ValueError, TypeError, AttributeError):
        pass