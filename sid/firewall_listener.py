from __future__ import annotations
import asyncio, re
from .alerts.base import AlertModule
from .utils import console
from .inputs.syslog_tail import journalctl_follow

class FirewallListener(AlertModule):
    name = "firewall_listener"
    def __init__(self, cfg, am, simulate: bool=False):
        super().__init__(cfg, am)
        self.filter = cfg.get("journalctl_filter","kernel")
        self.simulate = simulate

    async def run(self):
        if self.simulate:
            await self._simulate_loop()
            return
        async for line in journalctl_follow(self.filter):
            if "IN=" in line and ("DPT=" in line or "SPT=" in line):
                self.am.emit("LOW", self.name, "Kernel log packet event", {"line": line[:200]})

    async def _simulate_loop(self):
        import asyncio
        while True:
            self.am.emit("LOW", self.name, "Simulated firewall event", {"proto":"UDP","dpt":5353})
            await asyncio.sleep(15)
