import socket
import psutil
import platform
import subprocess
import re


class NetworkCollector:

    @staticmethod
    def get_local_ips_and_macs():
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        result = []

        for iface_name, addrs in interfaces.items():
            iface_data = {
                "interface": iface_name,
                "mac_address": None,
                "ipv4": None,
                "ipv6": None,
                "is_up": stats[iface_name].isup if iface_name in stats else None,
                "speed": stats[iface_name].speed if iface_name in stats else None,
                "mtu": stats[iface_name].mtu if iface_name in stats else None,
            }

            for addr in addrs:
                if addr.family == socket.AF_INET:
                    iface_data["ipv4"] = addr.address

                elif addr.family == socket.AF_INET6:
                    iface_data["ipv6"] = addr.address

                # MAC address (Windows/Linux)
                elif hasattr(psutil, "AF_LINK"):
                    if addr.family == psutil.AF_LINK:
                        iface_data["mac_address"] = addr.address

                else:
                    # fallback for Windows
                    if "mac" in addr.family.name.lower():
                        iface_data["mac_address"] = addr.address

            result.append(iface_data)

        return result

    @staticmethod
    def get_gateway():
        system = platform.system()

        try:
            if system == "Windows":
                output = subprocess.check_output("ipconfig", text=True)
                match = re.search(r"Default Gateway.*?:\s*([\d.]+)", output)
                return match.group(1) if match else None

            else:
                output = subprocess.check_output("ip route", shell=True, text=True)
                match = re.search(r"default via ([\d.]+)", output)
                return match.group(1) if match else None

        except Exception:
            return None

    @staticmethod
    def get_dns_servers():
        system = platform.system()

        dns_servers = []

        try:
            if system == "Windows":
                output = subprocess.check_output("ipconfig /all", text=True)

                dns_servers = re.findall(
                    r"DNS Servers[^\n]*:\s*([\d.]+)",
                    output
                )

                # Windows sometimes lists multiple DNS lines
                extra_dns = re.findall(r"\s+([\d.]+)", output)
                dns_servers.extend(extra_dns)

            else:
                with open("/etc/resolv.conf", "r") as f:
                    for line in f:
                        if "nameserver" in line:
                            dns_servers.append(line.split()[1])

        except Exception:
            pass

        return list(set(dns_servers))

    @staticmethod
    def get_network_io():
        io = psutil.net_io_counters()

        return {
            "bytes_sent": io.bytes_sent,
            "bytes_received": io.bytes_recv,
            "packets_sent": io.packets_sent,
            "packets_received": io.packets_recv,
            "errors_in": io.errin,
            "errors_out": io.errout,
            "drop_in": io.dropin,
            "drop_out": io.dropout,
        }

    @staticmethod
    def collect():
        return {
            "hostname": socket.gethostname(),
            "interfaces": NetworkCollector.get_local_ips_and_macs(),
            "gateway": NetworkCollector.get_gateway(),
            "dns_servers": NetworkCollector.get_dns_servers(),
            "network_io": NetworkCollector.get_network_io(),
        }