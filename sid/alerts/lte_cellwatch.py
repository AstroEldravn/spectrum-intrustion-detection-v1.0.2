from __future__ import annotations
import asyncio, yaml, json, re, random
from typing import Dict, Any, List, Tuple
from ..alerts.base import AlertModule
from ..utils import run_cmd

class LTECellWatch(AlertModule):
    name = "lte_cellwatch"
    def __init__(self, cfg, am, simulate: bool=False):
        super().__init__(cfg, am)
        self.whitelist_path = cfg.get("whitelist_path")
        self.simulate = simulate
        self.trusted = []
        if self.whitelist_path:
            try:
                self.trusted = yaml.safe_load(open(self.whitelist_path,"r"))["trusted"]
            except Exception:
                self.trusted = []

    async def run(self):
        if self.simulate:
            await self._simulate_loop()
            return
        rc, out, err = await run_cmd("LTE-Cell-Scanner -s -l")
        cells = self._parse_cells(out)
        for c in cells:
            if not self._trusted(c):
                self.am.emit("HIGH", self.name, "Untrusted LTE cell observed", c)

    def _trusted(self, cell: Dict[str, Any]) -> bool:
        for t in self.trusted:
            if all(str(cell.get(k)) == str(t.get(k)) for k in ("earfcn","pci","plmn")):
                return True
        return False

    def _parse_cells(self, text: str) -> List[Dict[str, Any]]:
        # Very crude parser; real tools output CSV or fixed columns
        cells = []
        for line in text.splitlines():
            m = re.search(r"EARFCN\s*(\d+).*PCI\s*(\d+).*PLMN\s*(\d+)", line)
            if m:
                cells.append({"earfcn": int(m.group(1)), "pci": int(m.group(2)), "plmn": m.group(3)})
        return cells

    async def _simulate_loop(self):
        while True:
            # occasionally fabricate an unknown cell
            c = {"earfcn": random.choice([6300, 150, 100]), "pci": random.randint(1,503), "plmn":"00101"}
            if not self._trusted(c):
                self.am.emit("HIGH", self.name, "Untrusted LTE cell observed (sim)", c)
            await asyncio.sleep(20)
