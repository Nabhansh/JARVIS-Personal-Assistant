# system_data_engine.py
import psutil
import time
import threading
from datetime import datetime

SYSTEM_STATE = {}

def get_cpu_temp():
    try:
        temps = psutil.sensors_temperatures()
        for name in temps:
            for entry in temps[name]:
                if entry.current:
                    return round(entry.current, 1)
    except:
        pass
    return None

def top_processes(n=5):
    procs = []
    for p in psutil.process_iter(['name', 'cpu_percent']):
        try:
            procs.append((p.info['name'], p.info['cpu_percent']))
        except:
            pass
    procs.sort(key=lambda x: x[1], reverse=True)
    return procs[:n]

def collect_system_data():
    battery = psutil.sensors_battery()
    net = psutil.net_io_counters()
    mem = psutil.virtual_memory()
    cpu_freq = psutil.cpu_freq()

    SYSTEM_STATE.update({
        "time": datetime.now().strftime("%H:%M:%S"),
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "cpu_freq": round(cpu_freq.current, 1) if cpu_freq else None,
        "cpu_temp": get_cpu_temp(),
        "memory_percent": mem.percent,
        "memory_used": round(mem.used / (1024**3), 2),
        "disk_percent": psutil.disk_usage("/").percent,
        "battery_percent": battery.percent if battery else None,
        "battery_plugged": battery.power_plugged if battery else None,
        "net_sent": net.bytes_sent,
        "net_recv": net.bytes_recv,
        "processes": top_processes()
    })

def system_data_loop(interval=1):
    while True:
        collect_system_data()
        time.sleep(interval)

def start_system_data_engine():
    t = threading.Thread(target=system_data_loop, daemon=True)
    t.start()