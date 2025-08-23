SHELL := /bin/bash
PY := python3
VENV := .venv

.PHONY: help
help:
	@echo "Targets:"
	@echo "  make bootstrap    - Create venv and install Python deps"
	@echo "  make deps-linux   - Install system deps on Debian/Ubuntu/Raspberry Pi"
	@echo "  make deps-macos   - Install system deps on macOS (brew)"
	@echo "  make deps-windows - Print Windows deps instructions (Chocolatey/Winget)"
	@echo "  make install      - Editable install (pip install -e .)"
	@echo "  make run          - Run SID with default config"
	@echo "  make sim          - Run SID in simulator mode"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Basic lint (ruff if available)"
	@echo "  make package      - Build wheel/sdist"

bootstrap:
	$(PY) -m venv $(VENV) && . $(VENV)/bin/activate && pip install -U pip && pip install -r requirements.txt

deps-linux:
	sudo ./scripts/linux_install.sh

deps-macos:
	./scripts/macos_install.sh

deps-windows:
	@echo "Use scripts\\windows_install.ps1 in an elevated PowerShell:"
	@echo "  powershell -ExecutionPolicy Bypass -File scripts\\windows_install.ps1"

install:
	$(PY) -m pip install -e .

run:
	sid-run -c configs/sid.yaml

sim:
	sid-sim -c configs/sid.yaml

test:
	$(PY) -m pytest -q

lint:
	@if command -v ruff >/dev/null 2>&1; then ruff check sid; else echo "ruff not installed"; fi

package:
	$(PY) -m build
