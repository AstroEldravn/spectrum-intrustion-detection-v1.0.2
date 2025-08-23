# Troubleshooting

- Run `sid-sim` first; if that works, sinks/config are fine.
- Wi‑Fi sniff needs root and monitor mode (`scripts/setup_monitor_mode.sh wlan0`).
- For SDR: verify tools run manually (e.g., `rtl_power -h`, `soapy_power -h`).
