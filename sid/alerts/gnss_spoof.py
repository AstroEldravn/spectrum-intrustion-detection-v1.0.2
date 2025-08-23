from __future__ import annotations
import asyncio, math
from typing import Dict, Any
from ..alerts.base import AlertModule
from ..inputs.gps_monitor import gpsd_stream

class GNSSSpoof(AlertModule):
    name = "gnss_spoof"
    def __init__(self, cfg, am, simulate: bool=False):
        super().__init__(cfg, am)
        self.addr = cfg.get("gpsd","localhost:2947")
        self.simulate = simulate

    async def run(self):
        if self.simulate:
            await self._simulate_loop()
            return
        host, port = (self.addr.split(":")+["2947"])[:2]
        async for obj in gpsd_stream(host, int(port)):
            if obj.get("class") == "TPV":
                hdop = obj.get("hdop", 0) or obj.get("eph", 0)
                if hdop and float(hdop) > 5:
                    self.am.emit("MEDIUM", self.name, "High HDOP indicates degraded GNSS",
                                 {"hdop": hdop})
            if obj.get("class") == "SKY":
                # sudden satellite set churn
                sats = obj.get("satellites", [])
                used = sum(1 for s in sats if s.get("used"))
                if used <= 3:
                    self.am.emit("HIGH", self.name, "Low satellites in use", {"used": used})

    async def _simulate_loop(self):
        while True:
            self.am.emit("MEDIUM", self.name, "GNSS anomaly (sim)", {"hdop": 6.2, "used": 3})
            await asyncio.sleep(30)
