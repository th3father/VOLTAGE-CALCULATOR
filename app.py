"""Flask web interface for the Ohm's law voltage calculator."""

from flask import Flask, render_template, request

from voltage import calculate_voltage, _parse_number

app = Flask(__name__)


def _build_chart_data(resistance, current):
    """Points of voltage vs. current for the given resistance, for the chart."""
    span = max(abs(current), 1) * 2
    step = span / 20
    currents = [round(-span + step * i, 4) for i in range(41)]
    voltages = [round(calculate_voltage(i, resistance), 4) for i in currents]
    return currents, voltages


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    current_input = ""
    resistance_input = ""
    chart_currents = []
    chart_voltages = []

    if request.method == "POST":
        current_input = request.form.get("current", "")
        resistance_input = request.form.get("resistance", "")
        try:
            current = _parse_number(current_input, "Current")
            resistance = _parse_number(resistance_input, "Resistance")
            voltage = calculate_voltage(current, resistance)
            result = f"{voltage:g}"
            chart_currents, chart_voltages = _build_chart_data(resistance, current)
        except ValueError as exc:
            error = str(exc)

    return render_template(
        "index.html",
        result=result,
        error=error,
        current_input=current_input,
        resistance_input=resistance_input,
        chart_currents=chart_currents,
        chart_voltages=chart_voltages,
    )


if __name__ == "__main__":
    app.run(debug=True)
