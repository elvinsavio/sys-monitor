import psutil
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class BatteryData:
    percentage: int
    is_plugged: bool
    minutes_left: Optional[int]
    status: str
    plugged_text: str


def get_battery_info():
    battery = psutil.sensors_battery()
    if not battery:
        return None

    if battery.power_plugged:
        status = "Charging" if battery.percent < 100 else "Fully Charged"
        plugged_text = "Plugged In"
    else:
        status = "Discharging"
        plugged_text = "Not Plugged In"

    data = BatteryData(
        percentage=battery.percent,
        is_plugged=battery.power_plugged,
        minutes_left=None if battery.secsleft <= 0 else round(battery.secsleft / 60),
        status=status,
        plugged_text=plugged_text,
    )
    return asdict(data)
