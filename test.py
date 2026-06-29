from telemetry import process ,system,network,service,registry

processes = process.ProcessCollector.get_processes()
system_info = system.SystemCollector.get_system_info()
network_info = network.NetworkCollector.collect()
service_info = service.ServiceCollector._get_windows_services()
registry_info = registry.SoftwareCollector.get_installed_software()
print(f"Total Processes : {len(processes)}")
print(f"System Info : {system_info}")
print(f"Network Info : {len(network_info)}")
print(f"Service Info : {len(service_info)}")
print("Registry info : ",registry_info)


# for process in processes[:10]:
#     print(process)



# for net in network_info:
#     print(net)