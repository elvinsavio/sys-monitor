import psutil
from dataclasses import dataclass
from typing import List


@dataclass
class ProcessInfo:
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    status: str


def get_top_processes(n: int = 10) -> List[ProcessInfo]:
    procs = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status"]):
        try:
            procs.append(
                ProcessInfo(
                    pid=proc.info["pid"],
                    name=proc.info["name"] or "?",
                    cpu_percent=round(proc.info["cpu_percent"] or 0.0, 1),
                    memory_percent=round(proc.info["memory_percent"] or 0.0, 1),
                    status=proc.info["status"],
                )
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    procs.sort(key=lambda p: (p.cpu_percent, p.memory_percent), reverse=True)
    return procs[:n]
