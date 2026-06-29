import winreg


class SoftwareCollector:

    UNINSTALL_PATHS = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
    ]

    @staticmethod
    def _read_registry(root, path):
        software_list = []

        try:
            key = winreg.OpenKey(root, path)
        except FileNotFoundError:
            return software_list

        i = 0
        while True:
            try:
                subkey_name = winreg.EnumKey(key, i)
                subkey_path = path + "\\" + subkey_name

                try:
                    subkey = winreg.OpenKey(root, subkey_path)

                    def get_value(name):
                        try:
                            value, _ = winreg.QueryValueEx(subkey, name)
                            return value
                        except FileNotFoundError:
                            return None

                    display_name = get_value("DisplayName")

                    # Skip entries without name (junk/system entries)
                    if not display_name:
                        i += 1
                        continue

                    software = {
                        "display_name": display_name,
                        "version": get_value("DisplayVersion"),
                        "publisher": get_value("Publisher"),
                        "install_location": get_value("InstallLocation"),
                        "install_date": get_value("InstallDate"),
                    }

                    software_list.append(software)

                except OSError:
                    pass

                i += 1

            except OSError:
                break

        return software_list

    @classmethod
    def get_installed_software(cls):
        all_software = []

        for path in cls.UNINSTALL_PATHS:
            all_software.extend(
                cls._read_registry(winreg.HKEY_LOCAL_MACHINE, path)
            )

        # Optional: include per-user installs
        all_software.extend(
            cls._read_registry(winreg.HKEY_CURRENT_USER,
                               r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        )

        return all_software