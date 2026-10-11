# Voltage Calculator

Calculates voltage from current and resistance using Ohm's law (V = I x R).
Includes a command-line interface and a Flask web interface.

Also calculates total resistance for resistors in series or in parallel,
with a "Total Resistance" section on the web page. Add or remove resistor
values, pick series or parallel, and see the total in ohms. A "Copy total
to voltage calculator" button carries that total straight into the
voltage calculator's resistance field.

## Install

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Test

```
pytest
```

## Run

Command line, with arguments:

```
python voltage.py 2 10
```

Command line, interactive:

```
python voltage.py
```

Web interface:

```
python app.py
```

Then open http://127.0.0.1:5000 in a browser.
