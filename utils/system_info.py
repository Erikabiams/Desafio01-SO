import psutil
import platform
import datetime

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_system_info():
    uname = platform.uname()
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    return uname, boot_time

def get_cpu_info():
    freq = psutil.cpu_freq()
    return {
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "max_frequency": freq.max,
        "min_frequency": freq.min,
        "current_frequency": freq.current
    }

def get_memory_info():
    virtual_mem = psutil.virtual_memory()
    return {
        "total": get_size(virtual_mem.total),
        "used": get_size(virtual_mem.used),
        "free": get_size(virtual_mem.available)
    }

def get_battery_info():
    bat = psutil.sensors_battery()
    return {
        "percent": bat.percent,
        "power_plugged": bat.power_plugged
    } if bat else None

def get_process_list():
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            processes.append(proc.info)
        except psutil.NoSuchProcess:
            continue
    return processes

def get_process_detail(pid):
    proc = psutil.Process(pid)
    with proc.oneshot():
        return {
            "name": proc.name(),
            "exe": proc.exe(),
            "status": proc.status(),
            "cpu_percent": proc.cpu_percent(interval=0.1),
            "memory_percent": proc.memory_percent(),
            "create_time": datetime.datetime.fromtimestamp(proc.create_time()).strftime("%Y-%m-%d %H:%M:%S")
        }
