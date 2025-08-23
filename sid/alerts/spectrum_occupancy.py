from __future__ import annotations
import asyncio, random
from typing import Dict, Any, List, Tuple
from ..alerts.base import AlertModule
from ..utils import run_cmd

class SpectrumOccupancy(AlertModule):
    name = "spectrum_occupancy"
    def __init__(self, cfg, am, simulate: bool=False):
        super().__init__(cfg, am)
        self.engine = cfg.get("engine","auto")
        self.step_db = float(cfg.get("step_db", 12))
        self.ranges = cfg.get("watch_ranges", [])
        self.simulate = simulate

    async def run(self):
        if self.simulate or not self.ranges:
            await self._simulate_loop()
            return
        for r in self.ranges:
            start, stop, step = float(r["start_mhz"]), float(r["stop_mhz"]), int(r["step_khz"])
            if self.engine in ("auto","rtl_power"):
                rc, out, err = await run_cmd(f"rtl_power -f {start}M:{stop}M:{step}k -i 1 -e 2 /dev/stdout")
            else:
                rc, out, err = await run_cmd(f"soapy_power -f {start}e6:{stop}e6 -r {step*1000} -F csv")
            # naive heuristic: look for big deltas in power values
            hits = out.count(",")  # just to have something to base on
            if hits > 0:
                self.am.emit("MEDIUM", self.name, "Spectrum activity observed",
                             {"range_mhz": [start, stop], "bins": hits})

    async def _simulate_loop(self):
        while True:
            for r in self.ranges or [{"start_mhz":433,"stop_mhz":435,"step_khz":50}]:
                activity = random.choice([0,0,0,1,2,3])
                if activity >= 2:
                    self.am.emit("MEDIUM", self.name, "Anomalous occupancy spike",
                                 {"range_mhz":[r["start_mhz"], r["stop_mhz"]], "score": activity})
            await asyncio.sleep(8)
