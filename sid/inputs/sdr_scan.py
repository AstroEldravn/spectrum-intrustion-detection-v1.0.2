from __future__ import annotations
import asyncio, re
from typing import AsyncIterator, Dict, List, Optional, Tuple
from ..utils import run_cmd

async def rtl_power_scan(start_mhz: float, stop_mhz: float, step_khz: int) -> Tuple[int, str, str]:
    cmd = f"rtl_power -f {start_mhz}M:{stop_mhz}M:{step_khz}k -i 1 -e 2 /dev/stdout"
    return await run_cmd(cmd)

async def soapy_power_scan(start_mhz: float, stop_mhz: float, step_khz: int) -> Tuple[int, str, str]:
    cmd = f"soapy_power -f {start_mhz}e6:{stop_mhz}e6 -r {step_khz*1000} -F csv"
    return await run_cmd(cmd)
