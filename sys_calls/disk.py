import psutil
import platform
import os
from dataclasses import dataclass, asdict
from typing import List, Dict


@dataclass
class DiskInfo:
    device: str
    mountpoint: str
    filesystem: str
    total_gb: float
    used_gb: float
    free_gb: float
    percentage: float
    is_system_disk: bool


def get_main_disk_report() -> Dict[str, any]:
    """
    Scans partitions and returns a dictionary structured for a front-end API.
    """
    # Identify the system root path based on OS
    system_root = "C:\\" if platform.system() == "Windows" else "/"

    report = {"system_disk": None, "other_disks": []}

    partitions = psutil.disk_partitions()

    for part in partitions:
        # Skip loopback and CD-ROMs with no data
        if "cdrom" in part.opts or not part.fstype:
            continue

        try:
            usage = psutil.disk_usage(part.mountpoint)

            # Create the dataclass instance
            is_main = part.mountpoint == system_root
            disk_data = DiskInfo(
                device=part.device,
                mountpoint=part.mountpoint
                if part.mountpoint == system_root
                else f"/.../{os.path.basename(part.mountpoint)}",
                filesystem=part.fstype,
                total_gb=round(usage.total / (1024**3), 2),
                used_gb=round(usage.used / (1024**3), 2),
                free_gb=round(usage.free / (1024**3), 2),
                percentage=usage.percent,
                is_system_disk=is_main,
            )

            # Categorize the disk
            if is_main:
                report["system_disk"] = asdict(disk_data)
            else:
                report["other_disks"].append(asdict(disk_data))
        except PermissionError:
            continue

    return report
