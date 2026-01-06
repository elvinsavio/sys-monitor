from dataclasses import dataclass
import psutil


@dataclass
class MemoryStats:
    # RAM Metrics
    ram_total: str
    ram_available: str
    ram_used: str
    ram_percent: float

    # Swap Metrics
    swap_total: str
    swap_free: str
    swap_used: str
    swap_percent: float


def get_memory_usage() -> MemoryStats:
    def to_gb(bytes_val):
        return f"{bytes_val / (1024**3):.2f} GB"

    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return MemoryStats(
        ram_total=to_gb(svmem.total),
        ram_available=to_gb(svmem.available),
        ram_used=to_gb(svmem.used),
        ram_percent=svmem.percent,
        swap_total=to_gb(swap.total),
        swap_free=to_gb(swap.free),
        swap_used=to_gb(swap.used),
        swap_percent=swap.percent,
    )
