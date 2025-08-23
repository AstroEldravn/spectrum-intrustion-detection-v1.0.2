#!/usr/bin/env bash
set -euo pipefail
IFACE=${1:-wlan0}
sudo ip link set "$IFACE" down
sudo iw "$IFACE" set monitor control
sudo ip link set "$IFACE" up
echo "Monitor mode enabled on $IFACE"
