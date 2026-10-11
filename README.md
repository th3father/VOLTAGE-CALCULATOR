# Voltage Calculator

Calculates voltage from current and resistance using Ohm's law (V = I x R).
Includes a command-line interface and a Flask web interface.

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
