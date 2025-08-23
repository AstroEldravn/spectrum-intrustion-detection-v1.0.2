from __future__ import annotations
import os, time, threading
from typing import Callable, Dict, Any, Optional

def sniff_deauth(iface: str, on_event: Callable[[Dict[str, Any]], None]) -> None:
    try:
        from scapy.all import sniff, Dot11, RadioTap  # type: ignore
    except Exception as e:
        raise RuntimeError("Scapy not available; install and run on Linux") from e

    def _cb(pkt):
        try:
            if pkt.haslayer(Dot11):
                dot11 = pkt.getlayer(Dot11)
                # subtype 12 = deauth, 10 = disassoc
                subtype = getattr(dot11, 'subtype', None)
                type_ = getattr(dot11, 'type', None)
                if type_ == 0 and subtype in (10,12):
                    ev = {
                        "fc_type": type_,
                        "fc_subtype": subtype,
                        "addr1": getattr(dot11, 'addr1', None),
                        "addr2": getattr(dot11, 'addr2', None),
                        "addr3": getattr(dot11, 'addr3', None),
                        "ts": time.time()
                    }
                    on_event(ev)
        except Exception:
            pass

    sniff(iface=iface, prn=_cb, store=False, monitor=True)
