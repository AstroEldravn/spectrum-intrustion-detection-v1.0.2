from __future__ import annotations
import asyncio, time, collections
from typing import Dict, Any
from ..alerts.base import AlertModule
from ..utils import console
from ..inputs.wifi_sniffer import sniff_deauth

class WifiDeauth(AlertModule):
    name = "wifi_deauth"
    def __init__(self, cfg, am, simulate: bool=False):
        super().__init__(cfg, am)
        self.iface = cfg.get("iface","wlan0")
        self.threshold = int(cfg.get("deauth_threshold_per_min", 10))
        self.simulate = simulate
        self.window = collections.deque(maxlen=1000)

    async def run(self):
        if self.simulate:
            await self._simulate_loop()
            return

        loop = asyncio.get_event_loop()
        def on_event(ev: Dict[str, Any]):
            self.window.append(ev["ts"])
            self._evaluate()
        await loop.run_in_executor(None, sniff_deauth, self.iface, on_event)

    def _evaluate(self):
        now = time.time()
        # window of last 60s
        while self.window and now - self.window[0] > 60:
            self.window.popleft()
        count = len(self.window)
        if count >= self.threshold:
            self.am.emit("HIGH", self.name, f"High deauth/disassoc rate: {count}/min",
                         {"count_last_min": count, "iface": self.iface})

    async def _simulate_loop(self):
        import random
        while True:
            # random deauth bursts
            burst = random.choices([0,1], weights=[0.8,0.2])[0]
            n = random.randint(0, self.threshold + 5) if burst else random.randint(0, 2)
            now = time.time()
            for _ in range(n):
                self.window.append(now)
            self._evaluate()
            await asyncio.sleep(5)
