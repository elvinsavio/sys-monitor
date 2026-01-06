import psutil
from dataclasses import dataclass
from typing import Tuple


@dataclass
class SystemLoadReport:
    tasks: int  # Total processes
    threads: int  # Total user-space threads
    running: int  # Tasks currently in 'running' state
    load_avg: Tuple[float, float, float]  # 1, 5, and 15 minute averages


def get_system_load_stats() -> SystemLoadReport:
    """
    Gathers process counts, thread counts, and system load averages.
    """
    total_tasks = 0
    total_threads = 0
    running_tasks = 0

    # Iterate over all running processes
    for proc in psutil.process_iter(["status", "num_threads"]):
        try:
            total_tasks += 1
            # Accessing info via the 'info' dict filled by process_iter
            total_threads += proc.info["num_threads"] or 0
            if proc.info["status"] == psutil.STATUS_RUNNING:
                running_tasks += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Process might die or be restricted during iteration
            continue

    # Load average: Returns (1min, 5min, 15min)
    # Note: On Windows, psutil simulates this by looking at CPU usage.
    load_avg = psutil.getloadavg()

    return SystemLoadReport(
        tasks=total_tasks,
        threads=total_threads,
        running=running_tasks,
        load_avg=load_avg,
    )
