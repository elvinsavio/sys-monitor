import psutil
from dataclasses import dataclass, asdict


@dataclass
class WifiData:
    interface: str
    is_up: bool
    ip_address: str
    upload_mb: float
    download_mb: float
    signal_strength: int  # Percentage 0-100


def _get_signal_strength(interface: str) -> int:
    try:
        with open("/proc/net/wireless", "r") as f:
            lines = f.readlines()
            for line in lines[2:]:  # Skip headers
                parts = line.split()
                if not parts:
                    continue

                # Check if this line is for our interface (remove colon if present)
                if_name = parts[0].strip(":")

                if if_name == interface:
                    # Link quality is usually the 3rd field (index 2) like "55."
                    quality = float(parts[2].replace(".", ""))
                    # Convert to percentage (assuming max 70 on most drivers)
                    percent = min(100, int((quality / 70) * 100))
                    return percent
    except Exception:
        pass
    return 0


def get_wifi_info():
    stats = psutil.net_if_stats()
    io_counters = psutil.net_io_counters(pernic=True)
    io_counters = psutil.net_io_counters(pernic=True)

    # Common Linux/Mac/Windows wireless prefixes
    # 'wl' covers wlp3s0, wlan0, etc.
    wifi_prefixes = ("wl", "wlan", "wi-fi", "wifi", "en0")

    for name, info in stats.items():
        if any(name.lower().startswith(pre) for pre in wifi_prefixes):
            # Check if the interface is actually active/up
            if info.isup:
                io = io_counters.get(name)

                # IP extraction removed as it is now masked (HIDDEN)

                data = WifiData(
                    interface=name,
                    is_up=info.isup,
                    ip_address="[HIDDEN]",
                    upload_mb=round(io.bytes_sent / (1024**2), 2),
                    download_mb=round(io.bytes_recv / (1024**2), 2),
                    signal_strength=_get_signal_strength(name),
                )
                return asdict(data)

    return None
