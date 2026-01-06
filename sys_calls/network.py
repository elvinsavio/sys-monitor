from dataclasses import dataclass
from typing import Optional
import psutil


@dataclass
class NetworkStats:
    interface: str
    rx_bytes: int
    tx_bytes: int

    @property
    def rx_mb(self) -> float:
        return round(self.rx_bytes / (1024**2), 2)

    @property
    def tx_mb(self) -> float:
        return round(self.tx_bytes / (1024**2), 2)


def get_session_data() -> Optional[NetworkStats]:
    """
    Auto-detects the primary active network interface and returns session stats.
    """
    stats = psutil.net_if_stats()
    io_counters = psutil.net_io_counters(pernic=True)

    # Priority list or heuristics
    # We want non-loopback, "up" interfaces.
    for name, info in stats.items():
        if name != "lo" and info.isup:
            # Found a candidate.
            if name in io_counters:
                io = io_counters[name]
                return NetworkStats(
                    interface=name, rx_bytes=io.bytes_recv, tx_bytes=io.bytes_sent
                )

    return None
