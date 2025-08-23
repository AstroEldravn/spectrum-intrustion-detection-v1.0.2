from __future__ import annotations
import asyncio, subprocess
from typing import AsyncIterator

async def journalctl_follow(match: str|None=None) -> AsyncIterator[str]:
    cmd = ["journalctl","-f","-n","0","-o","cat"]
    p = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    assert p.stdout
    while True:
        line = await p.stdout.readline()
        if not line: break
        s = line.decode(errors="replace").strip()
        if not match or (match in s):
            yield s
