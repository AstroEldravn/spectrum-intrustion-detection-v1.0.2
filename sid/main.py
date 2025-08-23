from __future__ import annotations
import asyncio, importlib, os, sys, logging
from typing import Dict, Any
import typer
from rich import print
from .config_loader import load_config
from .alert_manager import AlertManager
from .version import VERSION

app = typer.Typer(add_completion=False, help="Spectrum Intrusion Detection (SID)")

def build_modules(cfg, am, simulate: bool):
    mods = []
    mcfg = cfg.get("modules", {})
    if mcfg.get("wifi_deauth",{}).get("enabled"):
        from .alerts.wifi_deauth import WifiDeauth
        mods.append(WifiDeauth(mcfg.get("wifi_deauth",{}), am, simulate=simulate or cfg.get("simulate", False)))
    if mcfg.get("spectrum_occupancy",{}).get("enabled"):
        from .alerts.spectrum_occupancy import SpectrumOccupancy
        mods.append(SpectrumOccupancy(mcfg.get("spectrum_occupancy",{}), am, simulate=simulate or cfg.get("simulate", False)))
    if mcfg.get("lte_cellwatch",{}).get("enabled"):
        from .alerts.lte_cellwatch import LTECellWatch
        mods.append(LTECellWatch(mcfg.get("lte_cellwatch",{}), am, simulate=simulate or cfg.get("simulate", False)))
    if mcfg.get("gnss_spoof",{}).get("enabled"):
        from .alerts.gnss_spoof import GNSSSpoof
        mods.append(GNSSSpoof(mcfg.get("gnss_spoof",{}), am, simulate=simulate or cfg.get("simulate", False)))
    if mcfg.get("firewall_listener",{}).get("enabled"):
        from .firewall_listener import FirewallListener
        mods.append(FirewallListener(mcfg.get("firewall_listener",{}), am, simulate=simulate or cfg.get("simulate", False)))
    return mods

async def run_async(config_path: str, simulate: bool=False):
    cfg = load_config(config_path)
    am = AlertManager(cfg.get("sinks", []))
    mods = build_modules(cfg, am, simulate)
    if not mods:
        print("[yellow]No modules enabled. Edit configs/sid.yaml[/]")
        return
    tasks = [asyncio.create_task(m.run()) for m in mods]
    print(f"[bold green]SID v{VERSION}[/] running with {len(tasks)} module(s).")
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass

@app.command()
def run(c: str = typer.Option("configs/sid.yaml", "--config","-c", help="Path to config")):
    """Run SID with hardware (simulate value from config still applies per module)."""
    asyncio.run(run_async(c, simulate=False))

@app.command()
def simulate(c: str = typer.Option("configs/sid.yaml", "--config","-c", help="Path to config")):
    """Run SID in pure simulation mode (forces simulation on for all modules)."""
    asyncio.run(run_async(c, simulate=True))

# Backwards-compat names
run_command = run
simulate_command = simulate

if __name__ == "__main__":
    app()
