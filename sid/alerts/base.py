from __future__ import annotations
from typing import Dict, Any

class AlertModule:
    name = "base"
    def __init__(self, cfg, am):
        self.cfg = cfg
        self.am = am
    async def run(self):  # pragma: no cover - interface
        raise NotImplementedError
