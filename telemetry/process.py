import psutil
from datetime import datetime


class ProcessCollector:
    """
    Collects information about all running processes.

    This class only gathers telemetry.
    It does NOT communicate with the GUI.
    """

    @staticmethod
    def get_processes():
        processes = []

        for process in psutil.process_iter():

            try:
                with process.oneshot():

                    memory = process.memory_info()

                    process_data = {
                        "pid": process.pid,
                        "ppid": process.ppid(),
                        "name": process.name(),
                        "username": process.username(),
                        "status": process.status(),
                        "cpu_percent": process.cpu_percent(interval=None),
                        "memory_rss": memory.rss,
                        "memory_vms": memory.vms,
                        "threads": process.num_threads(),
                        "exe": process.exe(),
                        "create_time": datetime.fromtimestamp(
                            process.create_time()
                        ).strftime("%Y-%m-%d %H:%M:%S")
                    }

                    processes.append(process_data)

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                continue

            except Exception:
                continue

        return processes