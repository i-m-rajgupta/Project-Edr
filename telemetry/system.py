import platform
import socket
from datetime import datetime

import psutil


class SystemCollector:
    """
    Collects basic system information.

    This class only gathers telemetry.
    It does NOT communicate with the GUI.
    """

    @staticmethod
    def get_system_info():
        uname = platform.uname()

        print(uname)

        vm = psutil.virtual_memory()

        disk_partitions = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)

                disk_partitions.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "filesystem": partition.fstype,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent,
                })

            except PermissionError:
                continue

        boot_time = datetime.fromtimestamp(
            psutil.boot_time()
        ).strftime("%Y-%m-%d %H:%M:%S")

        system_info = {
            "hostname": socket.gethostname(),

            "windows_version": platform.system(),
            "build_number": platform.version(),

            "cpu_architecture": platform.machine(),
            "processor_name": platform.processor(),

            "total_ram": vm.total,
            "available_ram": vm.available,

            "disk_information": disk_partitions,

            "boot_time": boot_time,
        }

        return system_info