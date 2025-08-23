#!/usr/bin/env bash
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "Please run as root: sudo $0"
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y --no-install-recommends   git curl ca-certificates   python3 python3-venv python3-pip   rtl-sdr hackrf   soapysdr-tools libsoapysdr-dev soapyremote   gnuradio gr-osmosdr   gpsd gpsd-clients   aircrack-ng tshark   jq make

# udev rules for RTL-SDR to avoid root
if [[ -d /etc/udev/rules.d ]]; then
cat >/etc/udev/rules.d/20-rtlsdr.rules <<'EOF'
# RTL-SDR udev rules
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0bda", ATTRS{idProduct}=="2838", GROUP="plugdev", MODE="0666"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0bda", ATTRS{idProduct}=="2832", GROUP="plugdev", MODE="0666"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0bda", ATTRS{idProduct}=="283f", GROUP="plugdev", MODE="0666"
EOF
udevadm control --reload-rules || true
fi

echo "Done. Reconnect RTL-SDR devices if needed."
