#!/usr/bin/env bash
set -euo pipefail
if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew is required. Install from https://brew.sh"
  exit 1
fi

brew update
brew install python git gpsd gnuradio hackrf soapysdr aircrack-ng wireshark
echo "Note: some SDR tooling may need manual builds on macOS."
