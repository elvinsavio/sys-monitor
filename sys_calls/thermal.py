import psutil
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class TemperatureReading:
    sensor_name: str
    label: str
    current: float
    high: float | None
    critical: float | None


def get_thermal_stats() -> List[TemperatureReading]:
    """
    Retrieves temperature readings from all available hardware sensors.
    """
    thermal_readings = []

    # returns a dict: {'sensor_type': [shwtemp(label='', current=45.0, high=90.0, critical=100.0)]}
    temps = psutil.sensors_temperatures()

    for sensor_type, entries in temps.items():
        for entry in entries:
            thermal_readings.append(
                TemperatureReading(
                    sensor_name=sensor_type,
                    label=entry.label or sensor_type,
                    current=entry.current,
                    high=entry.high,
                    critical=entry.critical,
                )
            )

    return thermal_readings
