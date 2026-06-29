import psutil
import platform


class ServiceCollector:

    @staticmethod
    def _get_windows_services():
        if platform.system().lower() != "windows":
            raise NotImplementedError("Windows only")

        services = []

        for svc in psutil.win_service_iter():
            try:
                service_data = {
                    "service_name": None,
                    "display_name": None,
                    "status": None,
                    "startup_type": None,
                    "pid": None,
                    "executable_path": None,
                }

                # Safe individual calls (psutil can fail per-field)
                try:
                    service_data["service_name"] = svc.name()
                except Exception:
                    pass

                try:
                    service_data["display_name"] = svc.display_name()
                except Exception:
                    pass

                try:
                    service_data["status"] = svc.status()
                except Exception:
                    pass

                try:
                    service_data["startup_type"] = svc.start_type()
                except Exception:
                    pass

                # PID (only for running services)
                if service_data["status"] == "running":
                    try:
                        pid = svc.pid()
                        service_data["pid"] = pid

                        if pid:
                            try:
                                proc = psutil.Process(pid)
                                service_data["executable_path"] = proc.exe()
                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                pass
                    except Exception:
                        pass

                services.append(service_data)

            except Exception:
                # skip broken service entries safely
                continue

        return services