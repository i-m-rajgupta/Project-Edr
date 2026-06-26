import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess
import sys
import os


class HeartbeatService(win32serviceutil.ServiceFramework):
    _svc_name_ = "HeartbeatAgentService"
    _svc_display_name_ = "Edr Agent Service"
    _svc_description_ = "Edr Agent EXE as a Windows Service"

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)

        if self.process:
            servicemanager.LogInfoMsg("Stopping Heartbeat EXE...")
            self.process.terminate()

        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        servicemanager.LogInfoMsg("Heartbeat Service Started")

        # 🔴 PATH TO YOUR EXE (CHANGE THIS)
        exe_path = r"A:\Project AC\Dummy Edr\dist\EdrAgent.exe"

        # Start EXE as subprocess
        self.process = subprocess.Popen(
            exe_path,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        # Keep service alive
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(HeartbeatService)

# HEARTBEAT AGENT — WINDOWS SERVICE COMMANDS (PHASE 8 DOC)
# 1. PROJECT SETUP (FIRST TIME ONLY)

# Install dependencies:

# pip install pywin32 pyqt6

# Post-install setup (IMPORTANT):

# python -m pywin32_postinstall install
# 2. NAVIGATE TO PROJECT DIRECTORY
# cd "A:\Project AC\Dummy Edr"
# 3. INSTALL WINDOWS SERVICE

# Install service:

# python service.py install

# Enable auto-start on boot:

# sc config HeartbeatAgentService start= auto
# 4. START SERVICE

# Start via Python:

# python service.py start

# OR start via Windows:

# sc start HeartbeatAgentService
# 5. STOP SERVICE

# Stop via Python:

# python service.py stop

# OR stop via Windows:

# sc stop HeartbeatAgentService
# 6. RESTART SERVICE
# sc stop HeartbeatAgentService
# sc start HeartbeatAgentService
# 7. CHECK SERVICE STATUS

# Best method:

# sc.exe query HeartbeatAgentService

# Alternative:

# Get-Service HeartbeatAgentService
# 8. DEBUG MODE (IMPORTANT)

# Run service without Windows SCM:

# python service.py debug

# Use this for troubleshooting:

# service not running
# logs not updating
# EXE not starting
# 9. CHECK LOG FILE

# Open manually:

# notepad path\to\logfile.txt

# Or view in terminal:

# type logfile.txt
# 10. REMOVE / UNINSTALL SERVICE

# Stop service:

# sc stop HeartbeatAgentService

# Remove service:

# python service.py remove
# 11. RUN USER APPLICATION (TRAY + GUI)

# Start tray application:

# python app.py
# 12. SYSTEM ARCHITECTURE FLOW

# BOOT:

# Windows Service starts automatically
# Heartbeat engine runs in background
# Logs are continuously written

# USER LOGIN:

# Tray application starts manually
# User controls service (start/stop/restart)
# GUI reads logs in real-time
# 13. TROUBLESHOOTING COMMANDS

# Check service:

# sc query HeartbeatAgentService

# Force kill Python processes:

# taskkill /F /IM python.exe

# List all services:

# sc query type= service state= all
# 14. MOST IMPORTANT COMMANDS (QUICK LIST)
# python service.py install
# python service.py start
# python service.py stop
# python service.py remove
# sc.exe query HeartbeatAgentService
# sc config HeartbeatAgentService start= auto
# python service.py debug