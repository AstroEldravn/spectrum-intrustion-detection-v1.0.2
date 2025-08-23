#!/usr/bin/env bash
set -euo pipefail

PROFILE=${1:-field}   # field | hobbyist
SRC="configs/profiles/${PROFILE}.yaml"

if [[ ! -f "$SRC" ]]; then
  echo "Unknown profile: $PROFILE"
  exit 1
fi

# Default install paths
DEST_DIR="/etc/sid"
sudo mkdir -p "$DEST_DIR"
sudo cp "$SRC" "$DEST_DIR/sid.yaml"

# Optional LTE whitelist install if field profile
if [[ "$PROFILE" == "field" ]]; then
  if [[ -f "configs/rules/lte_whitelist.yaml" ]]; then
    sudo cp configs/rules/lte_whitelist.yaml "$DEST_DIR/lte_whitelist.yaml"
  fi
fi

echo "Applied profile '$PROFILE' to $DEST_DIR/sid.yaml"
echo "Run with: sudo sid-run -c $DEST_DIR/sid.yaml"
