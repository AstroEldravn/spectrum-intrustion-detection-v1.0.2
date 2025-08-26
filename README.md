[![Build](https://img.shields.io/badge/build-passing-brightgreen)](#)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](#)
[![Platforms](https://img.shields.io/badge/platforms-Linux%20%7C%20macOS%20%7C%20Windows-informational)](#)
[![Devices](https://img.shields.io/badge/SDR-RTL--SDR%20%7C%20HackRF%20%7C%20rtl_tcp-success)](#)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-ready-red)](#)

# Spectrum Intrusion Detection (SID) v1.0.2
* Added Field/Military as well as hobbyist profiles in configs/profiles
* Added Profile switcher: [scripts/apply_profile.sh]
* Added systemd installer: [scripts/install_systemd.sh]
* README updates with profile instructions and a Git/GitHub push + tag recipe prefilled for AstroEldravn/spectrum-ids

An intrusion detection system for the **electromagnetic spectrum**. SID ties together SDR sweeps, Wi‑Fi/LTE/GNSS observers, and host/network signals into a unified alert pipeline. It runs on Raspberry Pi, Debian/Ubuntu bare metal, and other Linux distributions, it should work on most flavors of Linux, but any Debian based derivative of Linux is where this *should* shine.; macOS isn't suggested but works for most features; Windows supports a subset.

## PIPELINE / COLLABORATION
- https://github.com/BPFLNALCR/sdr-watch
- sdr-watch is a Wideband scanner, baseline builder, and bandplan mapper for SDR devices with a lightweight web dashboard.
- Eventually I want to get this flipper spectrum companion to work in conjunction with the sdr-watch as this program has an intuitive WebGUI in development for visual categorization and multiple SDR use

> **Mission:** give defenders, hobbyists, and field teams a practical, scriptable, and *explainable* sensor that can flag RF anomalies: deauth floods, rogue LTE cells, GNSS spoofing symptoms, suspicious spectrum occupancy spikes, and more.

---

## Quick Start (Linux / Raspberry Pi)

```bash
# 1) System deps
make deps-linux

# 2) Python deps in a venv
make bootstrap

# 3) Install in editable mode
make install

# 4) Run in simulator mode to verify pipeline
make sim

# 5) Ready? Run for real (edit configs/sid.yaml first)
sudo make run
```

### One‑liners

```bash
# Debian/Ubuntu/Raspberry Pi
sudo ./scripts/linux_install.sh && python3 -m venv .venv && . .venv/bin/activate && pip install -U pip -r requirements.txt && pip install -e . && sid-sim -c configs/sid.yaml
```

> **TIP:** If you lack hardware today, set `simulate: true` in `configs/sid.yaml`. You’ll still exercise alerts, sinks, and logs.

---

## Hardware Support

- **RTL‑SDR (v3/v4)**: rtl-sdr, rtl\_power.
- **HackRF One**: libhackrf, SoapySDR.
- **SoapySDR radios**: SoapySDR, soapy\_power.
- **GNSS**: any GNSS receiver exposed through gpsd.
- **Wi‑Fi**: any interface that supports monitor mode (Linux).

---

## Features at a glance

- **Spectrum sweeps** via rtl\_power / soapy\_power → occupancy baselines → anomaly flags.
- **Wi‑Fi deauth/disassoc detection** (Scapy), + CSV fallback from `airodump-ng`/`tshark`.
- **LTE cell watch**: wrap external scanners (`LTE-Cell-Scanner`, `srsRAN cell_search`) → detect untrusted PCI/EARFCN.
- **GNSS spoofing heuristics** via gpsd (fix jumps, HDOP spikes, satellite set churn).
- **Syslog firewall ingest** (iptables/nftables) → correlation (optional).
- **Alert routing**: console, JSON log, file, syslog, MQTT, generic webhook.
- **Profiles** for hobbyist vs. field/military; per‑module enable/disable.
- **Simulator mode** for lab/CI without radios.
- **Systemd service** for unattended operation.

---

## Install System Dependencies

### Linux (Debian/Ubuntu/Raspberry Pi OS)

```bash
sudo ./scripts/linux_install.sh
```

What it installs (best effort): `rtl-sdr`, `hackrf`, `soapysdr-tools`, `libsoapysdr-dev`, `soapyremote`, `gnuradio`, `gr-osmosdr`, `gpsd`, `gpsd-clients`, `aircrack-ng`, `tshark`, `curl`, `git`, `python3-venv`.

### macOS

```bash
./scripts/macos_install.sh
```

Requires Homebrew; installs: `soapysdr`, `hackrf`, `gnuradio`, `gpsd`, `tshark`, `aircrack-ng` (where available).

### Windows

Open **elevated PowerShell** and run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\windows_install.ps1
```

Installs Chocolatey/Winget packages where possible and prints follow‑ups.

---

## Configure

Edit `configs/sid.yaml`. Minimal example:

```yaml
simulate: true           # set false to use hardware
profile: hobbyist

sinks:
  - type: console
  - type: file
    path: sid_events.jsonl

modules:
  wifi_deauth: {enabled: true}
  spectrum_occupancy: {enabled: true}
  lte_cellwatch: {enabled: false}
  gnss_spoof: {enabled: false}
  firewall_listener: {enabled: false}

rules:
  wifi_deauth:
    deauth_threshold_per_min: 10
  spectrum_occupancy:
    step_db: 12
    watch_ranges:
      - {start_mhz: 433, stop_mhz: 435, step_khz: 50}
      - {start_mhz: 860, stop_mhz: 900, step_khz: 100}

whitelists:
  wifi_bssid: ["AA:BB:CC:DD:EE:FF"]
  lte_cells:
    - {earfcn: 6300, pci: 123, plmn: "00101"}
```

See `configs/rules/` for more examples.

---

## Run

```bash
# Simulator mode exercises all pipelines without radios
sid-sim -c configs/sid.yaml

# Live mode (root recommended for Wi‑Fi/sniffers)
sudo sid-run -c configs/sid.yaml
```

### Systemd

```bash
sudo cp scripts/systemd/sid.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now sid
journalctl -u sid -f
```

---

## Outputs (Sinks)

- **console**: pretty Rich logs
- **file**: JSON lines (`sid_events.jsonl`)
- **syslog**: local syslog facility
- **mqtt**: `paho-mqtt` publish to a topic
- **webhook**: POST JSON to your endpoint

Each event includes `module`, `severity`, `message`, and `evidence` fields.

---

## Safety & Compliance

- You **must** follow local spectrum laws. Some modules only *observe* passively; others (Wi‑Fi monitor mode) require privileges.
- Never transmit. SID uses receive‑only flows.
- See `docs/Compliance.md` and `docs/Military-Usage.md`.

---

## Documentation

- `docs/Overview.md` – what SID is, how it works
- `docs/Quickstart.md` – step‑by‑step setup
- `docs/Hardware.md` – radios, antennas, GNSS, Wi‑Fi
- `docs/RF-Theory.md` – bands, modulation, noise, jamming
- `docs/Compliance.md` – legal & ethical use
- `docs/Military-Usage.md` – field notes & profiles
- `docs/Profiles.md` – tuning thresholds
- `docs/Recipes.md` – common tasks
- `docs/Troubleshooting.md` – fixes

---

## Roadmap (post‑1.0)

- Passive 5G NR cell watch
- Deep RF fingerprinting (ML)
- PCAP/PDML ingest pipeline
- Web UI
- Kubernetes/edge packaging

---

## Credits

Author: **Jonathan K. Fredlund** (AstroEldravn). MIT licensed.


---

## Profiles (Hobbyist vs Field/Military)

Two ready-to-use profiles live in `configs/profiles/`:

- `hobbyist.yaml` – simulator-friendly defaults, minimal sinks.
- `field.yaml` – receive-only, stricter thresholds, syslog/file sinks, GNSS + LTE enabled.

Apply one to `/etc/sid/sid.yaml`:

```bash
# From repo root
./scripts/apply_profile.sh field
# or
./scripts/apply_profile.sh hobbyist
```

Then run:
```bash
sudo sid-run -c /etc/sid/sid.yaml
```

---

## Systemd quick install

```bash
sudo ./scripts/install_systemd.sh
journalctl -u sid -f
```

---

## GitHub: initialize, tag, and push

```bash
git init
git branch -M main
git add .
git commit -m "feat: Spectrum Intrusion Detection v1.0.2"
git tag -a v1.0.0 -m "SID v1.0.0"

# Set your origin (SSH form shown)
git remote add origin git@github.com:AstroEldravn/spectrum-intrustion-detection-v1.0.2.git

# Or HTTPS:
# git remote add origin https://www.github.com/AstroEldravn/spectrum-intrustion-detection-v1.0.2.git

git push -u origin main --tags
```
