import pytest

from voltage import calculate_total_resistance, calculate_voltage, _parse_number


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


def test_total_resistance_series():
    assert calculate_total_resistance([10, 20, 30], "series") == 60


def test_total_resistance_parallel():
    assert calculate_total_resistance([10, 10], "parallel") == pytest.approx(5)


def test_total_resistance_single_resistor_series():
    assert calculate_total_resistance([42], "series") == 42


def test_total_resistance_single_resistor_parallel():
    assert calculate_total_resistance([42], "parallel") == 42


def test_total_resistance_decimals():
    assert calculate_total_resistance([1.5, 4.2], "series") == pytest.approx(5.7)


def test_total_resistance_parallel_decimals():
    assert calculate_total_resistance([2.5, 7.5], "parallel") == pytest.approx(1.875)


def test_total_resistance_parallel_with_zero():
    assert calculate_total_resistance([0, 10, 20], "parallel") == 0


def test_total_resistance_empty_list_raises():
    with pytest.raises(ValueError):
        calculate_total_resistance([], "series")


def test_total_resistance_negative_value_raises():
    with pytest.raises(ValueError):
        calculate_total_resistance([10, -5], "series")


def test_total_resistance_non_numeric_value_raises():
    with pytest.raises(ValueError):
        calculate_total_resistance([10, "abc"], "parallel")


def test_total_resistance_unknown_mode_raises():
    with pytest.raises(ValueError):
        calculate_total_resistance([10, 20], "bogus")
