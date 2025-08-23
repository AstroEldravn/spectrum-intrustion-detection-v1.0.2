from __future__ import annotations
import yaml, os, sys
from typing import Any, Dict

def load_config(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    # sensible defaults
    data.setdefault("simulate", False)
    data.setdefault("sinks", [{"type":"console"}])
    data.setdefault("modules", {})
    data.setdefault("whitelists", {})
    data.setdefault("log_level", "INFO")
    return data
