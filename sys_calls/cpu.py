import psutil
from dataclasses import dataclass
from typing import List


@dataclass
class CPUReport:
    physical_cores: int
    logical_cores: int
    total_load: float
    per_core_load: List[float]
    current_freq_mhz: float


def get_cpu_stats(interval: float = 1.0) -> CPUReport:
    """
    Gathers CPU metrics and returns a structured CPUReport.
    :param interval: Seconds to sample for CPU load.
    """
    # Get load first (takes 'interval' seconds)
    per_core = psutil.cpu_percent(interval=interval, percpu=True)
    total = psutil.cpu_percent()

    # Get counts and frequency
    physical = psutil.cpu_count(logical=False)
    logical = psutil.cpu_count(logical=True)
    freq = psutil.cpu_freq().current

    return CPUReport(
        physical_cores=physical,
        logical_cores=logical,
        total_load=total,
        per_core_load=per_core,
        current_freq_mhz=freq,
    )
