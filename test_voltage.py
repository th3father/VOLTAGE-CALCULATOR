import pytest

from voltage import calculate_voltage, _parse_number


def test_normal_values():
    assert calculate_voltage(2, 10) == 20


def test_decimals():
    assert calculate_voltage(1.5, 4.2) == pytest.approx(6.3)


def test_zero_current():
    assert calculate_voltage(0, 10) == 0


def test_zero_resistance():
    assert calculate_voltage(5, 0) == 0


def test_negative_current():
    assert calculate_voltage(-3, 10) == -30


def test_negative_resistance_raises():
    with pytest.raises(ValueError):
        calculate_voltage(5, -10)


def test_non_numeric_current_raises():
    with pytest.raises(ValueError):
        _parse_number("abc", "Current")


def test_non_numeric_resistance_raises():
    with pytest.raises(ValueError):
        _parse_number("xyz", "Resistance")
