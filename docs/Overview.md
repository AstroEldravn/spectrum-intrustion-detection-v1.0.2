# Overview

SID fuses readings from SDR sweeps, Wi‑Fi/LTE observers, GNSS, and host logs. A central `AlertManager` handles routing, deduplication, and serialization. Modules are independent coroutines, making it easy to add/remove sensors.
