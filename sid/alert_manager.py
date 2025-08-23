from __future__ import annotations
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import time, json, logging, socket
from pathlib import Path
import requests
import paho.mqtt.client as mqtt
from rich.console import Console
from .utils import json_dumps

console = Console()

@dataclass
class Event:
    ts: float
    severity: str
    module: str
    message: str
    evidence: Dict[str, Any] = field(default_factory=dict)

class Sink:
    def emit(self, ev: Event) -> None:
        raise NotImplementedError

class ConsoleSink(Sink):
    def emit(self, ev: Event) -> None:
        style = {"INFO":"green","LOW":"green","MEDIUM":"yellow","HIGH":"red","CRITICAL":"bold red"}.get(ev.severity,"white")
        console.print(f"[{style}]{ev.severity}[/] [{ev.module}] {ev.message}  {json_dumps(ev.evidence)}")

class FileSink(Sink):
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
    def emit(self, ev: Event) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json_dumps(ev.__dict__) + "\n")

class SyslogSink(Sink):
    def __init__(self, address: str="/dev/log"):
        # UDP syslog if not a unix socket path
        self.address = address
        if address.startswith("/"):
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        else:
            host, port = address.split(":") if ":" in address else (address, "514")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.address = (host, int(port))
    def emit(self, ev: Event) -> None:
        msg = f"<134>SID {ev.severity} {ev.module}: {ev.message} {json_dumps(ev.evidence)}"
        try:
            self.sock.sendto(msg.encode(), self.address)  # type: ignore[arg-type]
        except Exception as e:
            console.print(f"[red]SyslogSink error:[/] {e}")

class MQTTSink(Sink):
    def __init__(self, host: str, topic: str, port: int=1883, username: Optional[str]=None, password: Optional[str]=None):
        self.topic = topic
        self.client = mqtt.Client()
        if username: self.client.username_pw_set(username, password)
        self.client.connect(host, port, 60)
        self.client.loop_start()
    def emit(self, ev: Event) -> None:
        self.client.publish(self.topic, json_dumps(ev.__dict__), qos=0, retain=False)

class WebhookSink(Sink):
    def __init__(self, url: str):
        self.url = url
    def emit(self, ev: Event) -> None:
        try:
            requests.post(self.url, json=ev.__dict__, timeout=3)
        except Exception as e:
            console.print(f"[red]WebhookSink error:[/] {e}")

class AlertManager:
    def __init__(self, sinks_cfg: List[Dict[str, Any]]):
        self.sinks: List[Sink] = []
        for s in sinks_cfg:
            t = s.get("type","console")
            if t == "console":
                self.sinks.append(ConsoleSink())
            elif t == "file":
                self.sinks.append(FileSink(s.get("path","sid_events.jsonl")))
            elif t == "syslog":
                self.sinks.append(SyslogSink(s.get("address","/dev/log")))
            elif t == "mqtt":
                self.sinks.append(MQTTSink(s.get("host","127.0.0.1"), s.get("topic","sid/events"),
                                           s.get("port",1883), s.get("username"), s.get("password")))
            elif t == "webhook":
                self.sinks.append(WebhookSink(s.get("url","http://127.0.0.1:8000/ingest")))
        self.seen_keys = set()

    def emit(self, severity: str, module: str, message: str, evidence: Dict[str, Any]|None=None, dedupe_key: str|None=None):
        ev = Event(ts=time.time(), severity=severity, module=module, message=message, evidence=evidence or {})
        if dedupe_key:
            if dedupe_key in self.seen_keys: return
            self.seen_keys.add(dedupe_key)
        for s in self.sinks:
            try:
                s.emit(ev)
            except Exception as e:
                console.print(f"[red]Sink emit error:[/] {e}")
