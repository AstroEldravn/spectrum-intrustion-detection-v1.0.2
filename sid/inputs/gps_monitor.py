from __future__ import annotations
import asyncio, json, socket
from typing import AsyncIterator, Dict

# minimal gpsd watcher (text protocol)
async def gpsd_stream(host: str="127.0.0.1", port: int=2947) -> AsyncIterator[Dict]:
    reader, writer = await asyncio.open_connection(host, port)
    writer.write(b'?WATCH={"enable":true,"json":true}\n')
    await writer.drain()
    try:
        while True:
            line = await reader.readline()
            if not line:
                await asyncio.sleep(0.2)
                continue
            try:
                obj = json.loads(line.decode())
                yield obj
            except Exception:
                continue
    finally:
        writer.close()
        await writer.wait_closed()
