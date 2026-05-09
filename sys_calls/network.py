import time
from dataclasses import dataclass
from typing import Optional
import psutil


@dataclass
class NetworkStats:
    interface: str
    rx_bytes: int
    tx_bytes: int
    rx_rate_mbps: float
    tx_rate_mbps: float

    @property
    def rx_mb(self) -> float:
        return round(self.rx_bytes / (1024**2), 2)

    @property
    def tx_mb(self) -> float:
        return round(self.tx_bytes / (1024**2), 2)


_prev: dict = {}


def get_session_data() -> Optional[NetworkStats]:
    stats = psutil.net_if_stats()
    io_counters = psutil.net_io_counters(pernic=True)

    for name, info in stats.items():
        if name != "lo" and info.isup and name in io_counters:
            io = io_counters[name]
            now = time.monotonic()

            rx_rate = 0.0
            tx_rate = 0.0

            if name in _prev:
                prev_rx, prev_tx, prev_time = _prev[name]
                elapsed = now - prev_time
                if elapsed > 0:
                    rx_rate = max(0.0, (io.bytes_recv - prev_rx) / elapsed / (1024 ** 2))
                    tx_rate = max(0.0, (io.bytes_sent - prev_tx) / elapsed / (1024 ** 2))

            _prev[name] = (io.bytes_recv, io.bytes_sent, now)

            return NetworkStats(
                interface=name,
                rx_bytes=io.bytes_recv,
                tx_bytes=io.bytes_sent,
                rx_rate_mbps=round(rx_rate, 2),
                tx_rate_mbps=round(tx_rate, 2),
            )

    return None
