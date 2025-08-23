from __future__ import annotations
import asyncio, re, json
from typing import List, Dict, Tuple, Optional
from ..utils import run_cmd

# Best-effort wrappers; tools vary by distro.
async def lte_cell_scanner() -> Tuple[int, str, str]:
    # LTE-Cell-Scanner (https://github.com/SecUpwN/Android-IMSI-Catcher-Detector/wiki/LTE-Cell-Scanner)
    # On many systems it's installed as LTE-Cell-Scanner
    return await run_cmd("LTE-Cell-Scanner -s -l")

async def srsran_cell_search() -> Tuple[int, str, str]:
    return await run_cmd("cell_search --measurements")
