from __future__ import annotations
import asyncio, json, time, os, random
from typing import Any, Dict
from rich.console import Console

console = Console()

def now_ms() -> int:
    return int(time.time() * 1000)

def json_dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

def env_bool(name: str, default: bool=False) -> bool:
    v = os.getenv(name)
    if v is None: return default
    return v.strip().lower() in ("1","true","yes","y","on")

class RateLimit:
    def __init__(self, per_seconds: float, bucket: int=1):
        self.per = per_seconds
        self.bucket = bucket
        self.tokens = bucket
        self.last = time.time()

    def allow(self) -> bool:
        now = time.time()
        self.tokens = min(self.bucket, self.tokens + (now - self.last)/self.per)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

async def run_cmd(cmd: str) -> tuple[int, str, str]:
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await proc.communicate()
    return proc.returncode, out.decode(errors="replace"), err.decode(errors="replace")

def jitter(base: float, pct: float=0.15) -> float:
    return base * (1 + random.uniform(-pct, pct))
