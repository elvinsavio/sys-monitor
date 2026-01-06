import psutil
from dataclasses import dataclass
from typing import List


@dataclass
class FanReading:
    label: str
    rpm: int


def get_fan_stats() -> List[FanReading]:
    """
    Returns a list of current fan speeds.
    Note: Returns an empty list if no sensors are detected or unsupported (Windows).
    """
    fan_readings = []

    # psutil.sensors_fans() returns a dict: { 'device_name': [sfan, sfan] }
    sensors_data = psutil.sensors_fans()

    for device, entries in sensors_data.items():
        for entry in entries:
            fan_readings.append(
                FanReading(
                    label=entry.label or device,  # Use device name if label is empty
                    rpm=int(entry.current),
                )
            )

    return fan_readings
