from flask import Flask, render_template

from sys_calls.proc import SystemStats, get_system_stats
from sys_calls.ram import MemoryStats, get_memory_usage
from sys_calls.disk import DiskInfo, get_main_disk_report
from sys_calls.battery import BatteryData, get_battery_info
from sys_calls.wifi import WifiData, get_wifi_info

app = Flask(__name__)


@app.get("/")
def index():
    system_info: SystemStats = get_system_stats()

    return render_template("index.html", system_info=system_info)


@app.get("/mem")
def mem():
    memory_info: MemoryStats = get_memory_usage()

    return render_template("ram.html", memory_info=memory_info)


@app.get("/disk")
def disk():
    disk_info: DiskInfo = get_main_disk_report()

    return render_template("disk.html", disk_info=disk_info)


@app.get("/battery")
def battery():
    battery_info: BatteryData = get_battery_info()

    return render_template("battery.html", battery_info=battery_info)


@app.get("/wifi")
def wifi():
    wifi_info: WifiData = get_wifi_info()
    print(wifi_info)
    return render_template("wifi.html", wifi_info=wifi_info)
