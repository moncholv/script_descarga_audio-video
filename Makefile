VENV ?= venv
PY = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

.PHONY: venv install run build build-app build-gui binaries clean

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt pyinstaller

run:
	$(PY) script_descarga.py

# Descarga yt-dlp actualizado para macOS, Linux y Windows en binaries/
binaries:
	./scripts/update_binaries.sh

build: build-app

# App de terminal para macOS (dist/Moncho_YT.app)
build-app:
	$(VENV)/bin/pyinstaller --clean --noconfirm Moncho_YT_app.spec

# Interfaz gráfica opcional (dist-gui/Moncho_YT.app)
build-gui:
	$(VENV)/bin/pyinstaller --clean --noconfirm --distpath dist-gui --workpath build-gui Moncho_YT.spec

clean:
	rm -rf build build-gui dist dist-gui __pycache__ */__pycache__
