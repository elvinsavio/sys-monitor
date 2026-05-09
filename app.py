from flask import Flask, render_template
from sys_calls.proc import SystemStats, get_system_stats
from sys_calls.ram import MemoryStats, get_memory_usage
from sys_calls.disk import get_main_disk_report
from sys_calls.battery import BatteryData, get_battery_info
from sys_calls.wifi import WifiData, get_wifi_info
from sys_calls.cpu import CPUReport, get_cpu_stats
from sys_calls.fan import FanReading, get_fan_stats
from sys_calls.load import SystemLoadReport, get_system_load_stats
from sys_calls.thermal import TemperatureReading, get_thermal_stats
from sys_calls.network import NetworkStats, get_session_data
from sys_calls.top_procs import ProcessInfo, get_top_processes

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
    disk_info = get_main_disk_report()

    return render_template("disk.html", disk_info=disk_info)


@app.get("/battery")
def battery():
    battery_info: BatteryData = get_battery_info()

    return render_template("battery.html", battery_info=battery_info)


@app.get("/wifi")
def wifi():
    wifi_info: WifiData = get_wifi_info()
    return render_template("wifi.html", wifi_info=wifi_info)


@app.get("/cpu")
def cpu():
    cpu_info: CPUReport = get_cpu_stats(interval=0)
    return render_template("cpu.html", cpu_info=cpu_info)


@app.get("/fan")
def fan():
    fan_info: FanReading = get_fan_stats()
    return render_template("fan.html", fan_info=fan_info)


@app.get("/load")
def load():
    load_info: SystemLoadReport = get_system_load_stats()
    return render_template("load.html", load_info=load_info)


@app.get("/thermal")
def thermal():
    thermal_info: TemperatureReading = get_thermal_stats()
    return render_template("thermal.html", thermal_info=thermal_info)


@app.get("/network")
def network():
    net_info: NetworkStats = get_session_data()
    return render_template("network.html", net_info=net_info)


@app.get("/processes")
def processes():
    proc_list: list[ProcessInfo] = get_top_processes()
    return render_template("processes.html", proc_list=proc_list)
