"""Calculate voltage from current and resistance using Ohm's law (V = I x R)."""

import sys


def calculate_voltage(current, resistance):
    """Return voltage in volts given current (A) and resistance (ohms).

    Raises ValueError if resistance is negative.
    """
    if resistance < 0:
        raise ValueError("Resistance cannot be negative.")
    return current * resistance


def calculate_current(voltage, resistance):
    """Return current in amperes given voltage (V) and resistance (ohms).

    Raises ValueError if resistance is zero or negative.
    """
    if resistance == 0:
        raise ValueError("Resistance cannot be zero.")
    if resistance < 0:
        raise ValueError("Resistance cannot be negative.")
    return voltage / resistance


def calculate_total_resistance(resistances, mode):
    """Return total resistance in ohms for resistors in series or parallel.

    resistances is a list of numbers (or numeric strings). mode is
    "series" or "parallel". Raises ValueError for an empty list, a
    negative or non-numeric value, or an unknown mode.
    """
    if mode not in ("series", "parallel"):
        raise ValueError(f"Mode must be 'series' or 'parallel', got '{mode}'.")
    if not resistances:
        raise ValueError("At least one resistance value is required.")

    values = [_parse_number(r, "Resistance") for r in resistances]
    for value in values:
        if value < 0:
            raise ValueError("Resistance cannot be negative.")

    if mode == "series":
        return sum(values)

    if any(value == 0 for value in values):
        return 0.0
    return 1 / sum(1 / value for value in values)


def _parse_number(value, label):
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{label} must be a number, got '{value}'.")


def _format_voltage(voltage):
    return f"Voltage: {voltage:g} V"


def main():
    if len(sys.argv) == 3:
        current_raw, resistance_raw = sys.argv[1], sys.argv[2]
    elif len(sys.argv) == 1:
        current_raw = input("Enter current (A): ")
        resistance_raw = input("Enter resistance (ohms): ")
    else:
        print("Usage: python voltage.py [current resistance]")
        sys.exit(1)

    try:
        current = _parse_number(current_raw, "Current")
        resistance = _parse_number(resistance_raw, "Resistance")
        voltage = calculate_voltage(current, resistance)
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)

    print(_format_voltage(voltage))


if __name__ == "__main__":
    main()
