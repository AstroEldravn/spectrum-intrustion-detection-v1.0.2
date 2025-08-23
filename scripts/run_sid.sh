#!/usr/bin/env bash
set -euo pipefail
CONFIG=${1:-configs/sid.yaml}
exec sid-run -c "$CONFIG"
