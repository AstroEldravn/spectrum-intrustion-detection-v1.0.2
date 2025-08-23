#!/usr/bin/env bash
set -euo pipefail
UNIT_SRC="scripts/systemd/sid.service"
UNIT_DST="/etc/systemd/system/sid.service"
CONF_DST="/etc/sid/sid.yaml"

if [[ $EUID -ne 0 ]]; then
  echo "Please run as root: sudo $0"
  exit 1
fi

mkdir -p /etc/sid
if [[ ! -f "$CONF_DST" ]]; then
  cp configs/sid.yaml "$CONF_DST"
fi

cp "$UNIT_SRC" "$UNIT_DST"
systemctl daemon-reload
systemctl enable --now sid
systemctl status sid --no-pager -l || true
