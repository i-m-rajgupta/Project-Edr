import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from heartbeat import HeartbeatEngine
from log_viewer import LogViewer
from tray_controller import TrayController

LOG_FILE = Path("logs/data.log")

class AgentController:

    def __init__(self):
        self.app = QApplication(sys.argv)

        self.engine = HeartbeatEngine(
            log_file=LOG_FILE,
            interval=5
        )

        self.viewer = LogViewer()

        self.tray = TrayController(
            viewer=self.viewer,
            exit_callback=self.shutdown 
        )
        

    def start(self):
        print("[SYSTEM] Starting Heartbeat Agent")
        self.engine.start()
        return self.app.exec()
        

    def shutdown(self):
        print("[SYSTEM] Shutting down..")

        self.engine.stop()
        self.tray.hide()
        self.viewer.close()
        self.app.quit()

def main():
    controller = AgentController()

    exit_code = controller.start()
    print("[SYSTEM] Application exited")
    sys.exit(exit_code)
        

if __name__ == "__main__":
    main()

# ========================================
# 🟣 HEARTBEAT AGENT — PHASE 6 DOCUMENTATION
# FULL DAEMON ARCHITECTURE (PyQt6)
# ========================================

# PROJECT OVERVIEW
# ----------------------------------------
# Phase 6 transforms the Heartbeat Agent into a complete modular desktop daemon system.

# The application is now split into 4 independent components:

# 1. HeartbeatEngine (Background Worker)
# 2. LogViewer (UI Dashboard)
# 3. TrayController (System Control Layer)
# 4. AgentController (Main Orchestrator)

# This is a fully modular, production-style architecture.


# ========================================
# 🧠 SYSTEM ARCHITECTURE
# ========================================

#                 AgentController (CORE)
#                          │
#         ┌────────────────┼────────────────┐
#         │                │                │
#         ▼                ▼                ▼

# HeartbeatEngine     LogViewer      TrayController
# (Thread Worker)     (UI Layer)     (System Tray)

#                          │
#                          ▼

#                     logs/data.log


# ========================================
# 🚀 STARTUP FLOW
# ========================================

# 1. Application starts via main()

# 2. AgentController is created

# 3. QApplication is initialized

# 4. Components are created:
#    - HeartbeatEngine
#    - LogViewer
#    - TrayController

# 5. Heartbeat thread starts

# 6. Qt event loop starts (app.exec())


# FINAL STATE:
# - Background thread running
# - UI available
# - System tray active


# ========================================
# 🔵 HEARTBEAT ENGINE (BACKEND)
# ========================================

# FILE: heartbeat.py

# PURPOSE:
# Generates periodic heartbeat logs in background.


# THREAD FLOW:
# ----------------------------------------

# while not stop_event.is_set():
#     write_heartbeat()
#     sleep(interval)


# WRITE LOG FORMAT:
# ----------------------------------------

# timestamp | HEARTBEAT | System is running


# KEY FEATURES:
# ----------------------------------------
# ✔ Runs in background thread
# ✔ Non-blocking execution
# ✔ Safe shutdown using stop_event
# ✔ Clean thread join on exit


# START METHOD:
# ----------------------------------------

# self.thread = threading.Thread(target=heartbeat_worker)
# self.thread.start()


# STOP METHOD:
# ----------------------------------------

# stop_event.set()
# thread.join()


# ========================================
# 🟡 LOG VIEWER (UI DASHBOARD)
# ========================================

# FILE: log_viewer.py

# PURPOSE:
# Displays real-time log file content.


# UI COMPONENTS:
# ----------------------------------------
# ✔ QWidget (main window)
# ✔ QTextEdit (log display)
# ✔ QTimer (auto refresh system)


# LIVE UPDATE SYSTEM:
# ----------------------------------------

# self.timer = QTimer()
# self.timer.timeout.connect(self.load_logs)
# self.timer.start(1000)


# WORKFLOW:
# ----------------------------------------

# Read logs/data.log
#         ↓
# Load content
#         ↓
# Display in QTextEdit
#         ↓
# Scroll to bottom


# KEY FEATURE:
# ----------------------------------------
# ✔ No manual refresh required
# ✔ UI stays responsive
# ✔ File-based communication


# ========================================
# 🟣 SYSTEM TRAY CONTROLLER
# ========================================

# FILE: tray_controller.py

# PURPOSE:
# Provides system tray integration and controls.


# COMPONENTS:
# ----------------------------------------

# ✔ QSystemTrayIcon → tray icon
# ✔ QMenu → right-click menu
# ✔ QAction → clickable actions
# ✔ QIcon → icon system


# ----------------------------------------
# 🖼️ ICON SYSTEM
# ----------------------------------------

# FUNCTION:

# get_app_icon()


# LOGIC:

# Try:
#     assets/app_icon.png

# If valid:
#     use custom icon

# Else:
#     use Qt default icon


# BENEFIT:
# ✔ Prevents missing icon issues
# ✔ Adds branding support


# ----------------------------------------
# 📋 TRAY MENU
# ----------------------------------------

# Actions:

# 1. Show Window
# 2. Exit


# ----------------------------------------
# 🔗 SIGNAL CONNECTIONS
# ----------------------------------------

# Show Window → toggle_window()
# Exit → shutdown callback


# ----------------------------------------
# 🖱️ TRAY INTERACTION
# ----------------------------------------

# Double Click:
#     → toggle window


# Right Click:
#     → show menu


# ----------------------------------------
# 🪟 WINDOW TOGGLE LOGIC
# ----------------------------------------

# If window visible:
#     hide()

# Else:
#     show()
#     raise()
#     activateWindow()


# ========================================
# 🧠 AGENT CONTROLLER (CORE SYSTEM)
# ========================================

# FILE: app.py

# PURPOSE:
# Main system orchestrator.


# RESPONSIBILITIES:
# ----------------------------------------
# ✔ Initialize QApplication
# ✔ Create all modules
# ✔ Start heartbeat engine
# ✔ Manage system lifecycle
# ✔ Handle shutdown


# ----------------------------------------
# 🚀 START METHOD
# ----------------------------------------

# engine.start()
# app.exec()


# MEANING:
# - Start background thread
# - Start Qt event loop


# ----------------------------------------
# 🧯 SHUTDOWN METHOD
# ----------------------------------------

# engine.stop()
# tray.hide()
# viewer.close()
# app.quit()


# FLOW:
# ----------------------------------------

# Stop thread
# Hide tray
# Close UI
# Exit application


# ========================================
# 🔄 FULL SYSTEM EXECUTION FLOW
# ========================================

# START:
# ----------------------------------------

# main()
#   ↓
# AgentController created
#   ↓
# QApplication initialized
#   ↓
# Components created
#   ↓
# Heartbeat thread started
#   ↓
# Qt event loop started


# RUNNING STATE:
# ----------------------------------------

# HeartbeatEngine → writes logs every 5 sec
# LogViewer → reads logs every 1 sec
# TrayController → waits for user input


# USER ACTIONS:
# ----------------------------------------

# Tray → Show → Open window
# Tray → Hide → Close window
# Tray → Exit → Shutdown system


# SHUTDOWN:
# ----------------------------------------

# Stop thread
# Close UI
# Hide tray
# Exit Qt loop


# ========================================
# 🧠 CONCEPTS LEARNED
# ========================================

# ✔ Multithreading (background workers)
# ✔ Qt event-driven programming
# ✔ System tray integration
# ✔ Modular architecture design
# ✔ Separation of concerns
# ✔ File-based inter-process communication
# ✔ Clean shutdown handling
# ✔ Desktop daemon design pattern


# ========================================
# 🟢 FINAL RESULT
# ========================================

# The Heartbeat Agent is now a fully modular desktop daemon system.

# It includes:

# ✔ Background heartbeat engine
# ✔ Live log viewer dashboard
# ✔ System tray controller
# ✔ Central agent orchestrator
# ✔ Clean startup and shutdown lifecycle


# This completes Phase 6:
# FULL DAEMON ARCHITECTURE.
# ========================================