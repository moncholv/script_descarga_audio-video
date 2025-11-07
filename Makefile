VENV=venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: venv install run build clean

venv:
python3 -m venv $(VENV)

install: venv
$(PIP) install --upgrade pip
$(PIP) install -r requirements.txt
$(PIP) install pyinstaller

run:
$(PY) script_descarga.py

build:
$(VENV)/bin/pyinstaller Moncho_YT.spec

clean:
rm -rf build dist pycache */pycache

assets/Moncho_YT.icns

