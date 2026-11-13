from unittest.mock import patch
from hypothesis import given, strategies as st
from weather_alert import parse_reading, wind_category, rainfall_spread, main


@given(st.text() | st.none())
def test_parse_reading_no_crash(s):
    parse_reading(s)


@given(st.text() | st.none())
def test_wind_category_no_crash(s):
    wind_category(s)


@given(st.text() | st.none())
def test_rainfall_spread_no_crash(s):
    rainfall_spread(s)


def test_valid_branches():
    assert parse_reading("35.5/80") == (35.5, 80)
    assert parse_reading("35.5/80/10") is None
    assert parse_reading("bad/input") is None
    assert wind_category("95") == "warning"
    assert wind_category("45") == "advisory"
    assert wind_category("10") == "none"
    assert rainfall_spread("2,5.5,10") == 8.0


@patch("builtins.input", side_effect=["35.5/80", "45", "2,5.5,10"])
@patch("builtins.print")
def test_main(mock_print, mock_input):
    main()