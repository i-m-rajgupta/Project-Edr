import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from heartbeat import HeartbeatEngine
from log_viewer import LogViewer
from tray_controller import TrayController


from config import LOG_FILE

class AgentController:

    def __init__(self):
        self.app = QApplication(sys.argv)

        self.engine = HeartbeatEngine(
            log_file=LOG_FILE,
            interval=5
        )

        self.app.setQuitOnLastWindowClosed(False)

        self.gui_factory = lambda: LogViewer()

        self.tray = TrayController(
            gui_factory=self.gui_factory,
            exit_callback=self.shutdown 
        )
        

    def start(self):
        print("[SYSTEM] Starting Daemon Agent")
        self.engine.start()
        return self.app.exec()
        

    def shutdown(self):
        print("[SYSTEM] Shutting down..")

        self.engine.stop()
        self.tray.hide()
        if self.tray.viewer:
            self.tray.viewer.close()
        self.app.quit()
        print("[SYSTEM] Agent stopped cleanly")

def main():
    controller = AgentController()
    exit_code = controller.start()
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


# ========================================
# 🔵 HEARTBEAT AGENT — PHASE 7 DOCUMENTATION
# REAL DAEMON ARCHITECTURE (PyQt6)
# ========================================

# PROJECT OVERVIEW
# ----------------------------------------
# Phase 7 transforms the system from a "desktop app with background thread"
# into a TRUE DAEMON-STYLE ARCHITECTURE.

# Key Idea:
# ✔ Engine runs always (independent service)
# ✔ Tray runs always (control layer)
# ✔ GUI is optional (on-demand tool)


# ========================================
# 🧠 WHY PHASE 7 EXISTS
# ========================================

# Before Phase 7:
# ----------------------------------------
# GUI + Tray + Engine = tightly connected system

# Problems:
# ❌ GUI lifecycle affects backend
# ❌ Closing window may stop system
# ❌ App behaves like a normal desktop program
# ❌ No true background operation


# After Phase 7:
# ----------------------------------------
# Each component becomes independent:

# ✔ HeartbeatEngine → ALWAYS running
# ✔ TrayController   → ALWAYS running
# ✔ LogViewer        → ON DEMAND ONLY


# RESULT:
# ✔ System behaves like a real background agent
# ✔ GUI is no longer required for operation


# ========================================
# 🏗 SYSTEM ARCHITECTURE (PHASE 7)
# ========================================

#                 AgentController (CORE)
#                          │
#         ┌────────────────┼────────────────┐
#         │                │                │
#         ▼                ▼                ▼

# HeartbeatEngine     TrayController     LogViewer
# (Always Running)    (Always Active)    (On Demand)


# DATA FLOW:
# ----------------------------------------
# HeartbeatEngine → writes logs → data/log.txt → LogViewer reads


# ========================================
# 🚀 STARTUP FLOW
# ========================================

# 1. main() executes
# 2. AgentController is created
# 3. QApplication starts
# 4. HeartbeatEngine starts thread
# 5. TrayController initializes system tray
# 6. GUI is NOT created initially

# FINAL STATE:
# ✔ Background engine running
# ✔ Tray active
# ✔ GUI idle (not created)


# ========================================
# 🔵 HEARTBEAT ENGINE (DAEMON CORE)
# ========================================

# FILE: heartbeat.py

# PURPOSE:
# Background service that continuously writes system status logs.


# THREAD BEHAVIOR:
# ----------------------------------------

# while not stop_event.is_set():
#     write_heartbeat()
#     sleep(interval)


# LOG FORMAT:
# ----------------------------------------
# timestamp | HEARTBEAT | System is running


# FEATURES:
# ----------------------------------------
# ✔ Independent of GUI
# ✔ Runs in background thread
# ✔ Controlled via stop_event
# ✔ Safe shutdown using thread join()


# START FLOW:
# ----------------------------------------
# Thread created → started → runs forever


# STOP FLOW:
# ----------------------------------------
# stop_event.set()
# thread.join()


# RESULT:
# ✔ True background service behavior


# ========================================
# 🟡 TRAY CONTROLLER (CONTROL LAYER)
# ========================================

# FILE: tray_controller.py

# PURPOSE:
# System control interface using OS system tray.


# COMPONENTS USED:
# ----------------------------------------

# ✔ QSystemTrayIcon → tray icon
# ✔ QMenu → right-click menu
# ✔ QAction → clickable menu items
# ✔ QIcon → icon handling


# ========================================
# 🖼 ICON SYSTEM
# ========================================

# FUNCTION:
# get_app_icon()

# LOGIC:
# ----------------------------------------
# Try:
#     assets/app_icon.png

# If valid:
#     use custom icon

# Else:
#     fallback to Qt default icon


# BENEFIT:
# ✔ Prevents missing icon crash
# ✔ Allows branding support


# ========================================
# 📋 TRAY MENU SYSTEM
# ========================================

# Menu Options:
# ----------------------------------------
# 1. Open Log Viewer
# 2. Exit


# BEHAVIOR:
# ----------------------------------------
# Open Log Viewer → toggles GUI creation
# Exit → shuts down entire system


# ========================================
# 🧠 GUI LAZY LOADING (IMPORTANT CHANGE)
# ========================================

# KEY IDEA:
# GUI is NOT created at startup.

# Instead:

# ✔ Created only when user clicks tray


# LOGIC:
# ----------------------------------------
# if viewer is None:
#     viewer = create_gui()


# BENEFIT:
# ✔ Saves memory
# ✔ Improves startup speed
# ✔ Enables true daemon behavior


# ========================================
# 🖱 TRAY INTERACTIONS
# ========================================

# Double Click:
# ----------------------------------------
# → Open / Close Log Viewer


# Right Click:
# ----------------------------------------
# → Show menu


# ========================================
# 🟢 WINDOW TOGGLE LOGIC
# ========================================

# If GUI visible:
#     hide()

# Else:
#     show()
#     raise()
#     activateWindow()


# FEATURE:
# ✔ GUI does not control lifecycle anymore
# ✔ Only visibility is controlled


# ========================================
# 🟣 AGENT CONTROLLER (CORE SYSTEM)
# ========================================

# FILE: app.py

# ROLE:
# Main orchestrator of entire system.


# RESPONSIBILITIES:
# ----------------------------------------
# ✔ Create QApplication
# ✔ Start HeartbeatEngine
# ✔ Initialize TrayController
# ✔ Manage shutdown lifecycle


# ========================================
# 🚀 START METHOD FLOW
# ========================================

# engine.start()
# app.exec()


# MEANING:
# ----------------------------------------
# ✔ Engine starts background thread
# ✔ Qt event loop starts
# ✔ Tray becomes active system controller


# ========================================
# 🧯 SHUTDOWN FLOW
# ========================================

# Triggered by:
# ----------------------------------------
# ✔ Tray Exit button
# ✔ System shutdown call


# PROCESS:
# ----------------------------------------
# 1. Stop heartbeat thread
# 2. Hide tray
# 3. Close GUI if open
# 4. Quit QApplication


# RESULT:
# ✔ Clean shutdown
# ✔ No zombie threads


# ========================================
# 🔄 FULL SYSTEM BEHAVIOR (PHASE 7)
# ========================================

# RUNNING STATE:
# ----------------------------------------

# HeartbeatEngine → always running
# TrayController   → always active
# LogViewer        → only when opened


# USER ACTIONS:
# ----------------------------------------

# Tray Click:
#     → Open/Close GUI

# Exit:
#     → Stop engine + quit app

# GUI Close:
#     → DOES NOT STOP SYSTEM


# ========================================
# 🧠 KEY CONCEPTS LEARNED
# ========================================

# ✔ True background daemon design
# ✔ Lazy GUI initialization
# ✔ Separation of system components
# ✔ OS-level system tray integration
# ✔ Event-driven architecture
# ✔ Thread-safe lifecycle control
# ✔ Real-world agent design pattern


# ========================================
# 🟢 FINAL RESULT
# ========================================

# Phase 7 achieves a real daemon system:

# ✔ Heartbeat runs independently
# ✔ Tray always active
# ✔ GUI is optional
# ✔ System survives window closing
# ✔ Clean shutdown lifecycle


# ========================================
# 🚀 PHASE 7 CONCLUSION
# ========================================

# Phase 7 is the transformation point:

# FROM:
#     GUI-based Python app

# TO:
#     Background agent system (daemon architecture)


# This is the same design pattern used in:
# ✔ Discord
# ✔ Google Drive
# ✔ Steam
# ✔ Antivirus software
# ✔ System monitors

# ========================================