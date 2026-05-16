"""System Monitor - Collects real-time system information."""

import platform
import psutil
from datetime import datetime


class SystemMonitor:
    """Monitors system resources and provides system information."""

    @staticmethod
    def get_cpu_percent() -> float:
        return psutil.cpu_percent(interval=0.1)

    @staticmethod
    def get_memory_info() -> dict:
        mem = psutil.virtual_memory()
        return {
            "total_gb": round(mem.total / (1024 ** 3), 1),
            "used_gb": round(mem.used / (1024 ** 3), 1),
            "percent": mem.percent,
        }

    @staticmethod
    def get_disk_info() -> dict:
        disk = psutil.disk_usage("/")
        return {
            "total_gb": round(disk.total / (1024 ** 3), 1),
            "used_gb": round(disk.used / (1024 ** 3), 1),
            "percent": round(disk.percent, 1),
        }

    @staticmethod
    def get_battery_info() -> dict | None:
        battery = psutil.sensors_battery()
        if battery is None:
            return None
        return {
            "percent": round(battery.percent, 1),
            "plugged": battery.power_plugged,
        }

    @staticmethod
    def get_network_info() -> dict:
        net = psutil.net_io_counters()
        return {
            "sent_mb": round(net.bytes_sent / (1024 ** 2), 1),
            "recv_mb": round(net.bytes_recv / (1024 ** 2), 1),
        }

    @staticmethod
    def get_system_info() -> dict:
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor() or "N/A",
            "python": platform.python_version(),
            "hostname": platform.node(),
        }

    @staticmethod
    def get_datetime_info() -> dict:
        now = datetime.now()
        return {
            "date": now.strftime("%d %B %Y"),
            "time": now.strftime("%H:%M:%S"),
            "day": now.strftime("%A"),
        }

    @staticmethod
    def get_uptime() -> str:
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}m {seconds}s"

    def get_all_stats(self) -> dict:
        return {
            "cpu": self.get_cpu_percent(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "battery": self.get_battery_info(),
            "network": self.get_network_info(),
            "system": self.get_system_info(),
            "datetime": self.get_datetime_info(),
            "uptime": self.get_uptime(),
        }
