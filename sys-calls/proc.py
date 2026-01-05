import os
import platform
import re
import subprocess
from dataclasses import dataclass, field
from typing import List

import psutil


@dataclass(frozen=True)
class SystemStats:
    """Object containing structured system information."""

    distro: str
    kernel: str
    uptime_hours: int
    uptime_minutes: int
    memory_used_mib: int
    memory_total_mib: int
    cpu_model: str
    gpu_info: List[str]
    desktop_environment: str
    shell: str

    def __str__(self):
        """Custom string representation for easy printing."""
        gpus = ", ".join(self.gpu_info)
        return (
            f"OS:     {self.distro}\n"
            f"Kernel: {self.kernel}\n"
            f"Uptime: {self.uptime_hours}h {self.uptime_minutes}m\n"
            f"DE:     {self.desktop_environment}\n"
            f"Shell:  {self.shell}\n"
            f"CPU:    {self.cpu_model}\n"
            f"Memory: {self.memory_used_mib}MiB / {self.memory_total_mib}MiB\n"
            f"GPUs:   {gpus}"
        )


def get_gpu_info() -> List[str]:
    try:
        # -mm provides machine-readable output
        output = subprocess.check_output(["lspci", "-mm"], text=True)
        gpus = []
        for line in output.splitlines():
            if "VGA" in line or "3D" in line:
                parts = re.findall(r'"([^"]*)"', line)
                if len(parts) >= 3:
                    # parts[1] is Vendor, parts[2] is Model/Device
                    gpus.append(f"{parts[1]} {parts[2]}")
        return gpus if gpus else ["Unknown GPU"]
    except Exception:
        return ["Could not detect GPU"]


def get_system_stats() -> SystemStats:
    # 1. OS and Kernel
    try:
        distro = platform.freedesktop_os_release().get("PRETTY_NAME", "Linux")
    except AttributeError:
        distro = platform.system()

    kernel = platform.release()

    # 2. Uptime
    with open("/proc/uptime", "r") as f:
        uptime_seconds = float(f.readline().split()[0])
        hours, remainder = divmod(int(uptime_seconds), 3600)
        minutes, _ = divmod(remainder, 60)

    # 3. Memory (Converted to MiB)
    mem = psutil.virtual_memory()
    mem_used = mem.used // (1024**2)
    mem_total = mem.total // (1024**2)

    # 4. Hardware
    # Note: platform.processor() often returns empty on Linux;
    # check /proc/cpuinfo or use psutil if needed.
    cpu_model = platform.processor() or "Unknown CPU"
    gpu_info = get_gpu_info()

    # 5. Environment
    de = os.environ.get("XDG_CURRENT_DESKTOP", "Unknown")
    shell = os.environ.get("SHELL", "").split("/")[-1]

    return SystemStats(
        distro=distro,
        kernel=kernel,
        uptime_hours=hours,
        uptime_minutes=minutes,
        memory_used_mib=mem_used,
        memory_total_mib=mem_total,
        cpu_model=cpu_model,
        gpu_info=gpu_info,
        desktop_environment=de,
        shell=shell,
    )
