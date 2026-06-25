from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit
from PyQt6.QtCore import QTimer


LOG_FILE = Path("logs/data.log")

class LogViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Heartbeat Log Viewer")
        self.setGeometry(300,200,700,500)

        layout = QVBoxLayout()

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        layout.addWidget(self.log_area)
        self.setLayout(layout)

        self.load_logs()

        self.timer = QTimer()
        self.timer.timeout.connect(self.load_logs)
        self.timer.start(1000)
        
        self.hide()

    def load_logs(self):
        if LOG_FILE.exists():
            try:
                with open(LOG_FILE,"r",encoding="utf-8") as file:
                    content = file.read()

                self.log_area.setText(content)

                self.log_area.verticalScrollBar().setValue(
                    self.log_area.verticalScrollBar().maximum()
                )

            except Exception as e:
                self.log_area.setText(f"Error reading log file : {e}")

        else:
            self.log_area.setText("Log file not found.") 
   

# ========================================
# 🟢 HEARTBEAT AGENT — PHASE 3 DOCUMENTATION
# LOG VISUALIZATION INTERFACE (PyQt6)
# ========================================

# 🎯 OBJECTIVE OF PHASE 3
# ----------------------------------------
# Phase 3 introduces a graphical user interface (GUI) for the Heartbeat Agent.

# The goals are:

# ✔ Create a desktop window using PyQt6
# ✔ Read logs/data.log generated in Phase 2
# ✔ Display log content in a GUI window
# ✔ Allow manual refresh of logs
# ✔ Keep Phase 2 heartbeat running in background

# IMPORTANT:
# - GUI is static (no auto-refresh yet)
# - Live updates will be added in Phase 4


# ========================================
# 🧠 SYSTEM ARCHITECTURE (PHASE 3)
# ========================================

# PHASE 2 (BACKEND - HEARTBEAT SYSTEM)
# ----------------------------------------
# Heartbeat Worker Thread
#         ↓
# Writes logs into file:
# logs/data.log


# PHASE 3 (FRONTEND - GUI VIEWER)
# ----------------------------------------
# PyQt6 GUI Application
#         ↓
# Reads logs/data.log
#         ↓
# Displays logs in window


# KEY IDEA:
# ----------------------------------------
# ✔ Phase 2 generates data
# ✔ Phase 3 consumes data
# ✔ Communication happens via file system

# This is called:
# ➡ File-based communication (IPC concept)


# ========================================
# ⚙️ WHAT CHANGED IN PHASE 3
# ========================================

# BEFORE (Phase 2 only):
# ----------------------------------------
# ✔ Logs printed in terminal
# ✔ Logs stored in file
# ❌ No visual interface


# NOW (Phase 3 added):
# ----------------------------------------
# ✔ Desktop GUI window
# ✔ Log file displayed visually
# ✔ Manual refresh button added
# ✔ Independent from heartbeat engine


# ========================================
# 📦 REQUIREMENTS
# ========================================

# Install PyQt6:

# pip install PyQt6


# ========================================
# 🧱 CORE COMPONENTS
# ========================================

# 1. QApplication
# ----------------------------------------
# Starts Qt GUI system and event loop.

# app = QApplication(sys.argv)

# Without this, GUI cannot run.


# 2. QWidget
# ----------------------------------------
# Main window container.

# class LogViewer(QWidget):

# Represents the application window.


# 3. QVBoxLayout
# ----------------------------------------
# Arranges UI elements vertically.

# layout = QVBoxLayout()


# 4. QTextEdit (Log Display)
# ----------------------------------------
# Displays logs in scrollable text box.

# self.log_area = QTextEdit()
# self.log_area.setReadOnly(True)


# 5. QPushButton (Refresh Button)
# ----------------------------------------
# Manually reloads log file.

# self.refresh_button = QPushButton("Load Logs")
# self.refresh_button.clicked.connect(self.load_logs)


# ========================================
# 📂 LOG LOADING MECHANISM
# ========================================

# FUNCTION: load_logs()
# ----------------------------------------

# STEP 1: Check file exists
# ----------------------------------------
# if LOG_FILE.exists():

# Prevents program crash if file is missing.


# STEP 2: Read file content
# ----------------------------------------
# with open(LOG_FILE, "r", encoding="utf-8") as file:
#     content = file.read()


# STEP 3: Display in GUI
# ----------------------------------------
# self.log_area.setText(content)


# STEP 4: Error handling
# ----------------------------------------
# except Exception as e:
#     self.log_area.setText("Error reading log file")


# ========================================
# 🖥️ PROGRAM FLOW
# ========================================

# 1. Start Python script
# 2. Initialize QApplication
# 3. Create LogViewer window
# 4. Setup UI components
# 5. Load logs from file
# 6. Display logs in window
# 7. Wait for user interaction
# 8. Refresh button reloads logs

# ========================================
# 🧪 OUTPUT

# GUI Window:
# ----------------------------------------

# +--------------------------------------+
# | Heartbeat Log Viewer                |
# |--------------------------------------|
# | 2026-06-25 10:00:00 | HEARTBEAT     |
# | 2026-06-25 10:00:05 | HEARTBEAT     |
# | 2026-06-25 10:00:10 | HEARTBEAT     |
# |                                      |
# | [ Load Logs ]                       |
# +--------------------------------------+

# ========================================
# 🧠 KEY CONCEPTS LEARNED
# ========================================

# 1. Separation of Systems
# ----------------------------------------
# Phase 2 → Generates data
# Phase 3 → Displays data

# This is real system architecture design.


# 2. File-Based Communication
# ----------------------------------------
# Heartbeat writes → GUI reads

# No direct function calls required.


# 3. Event-Driven Programming
# ----------------------------------------
# Qt uses event loop:

# app.exec()

# GUI reacts to user actions instead of running loops.


# 4. IMPORTANT RULE
# ----------------------------------------
# ❌ Do NOT use infinite loops in GUI
# ❌ Do NOT block main thread
# ✔ Qt controls execution flow


# ========================================
# 🟡 PHASE 3 SUCCESS CRITERIA
# ========================================

# ✔ GUI window opens successfully
# ✔ Logs are displayed correctly
# ✔ Refresh button works
# ✔ Phase 2 heartbeat continues running
# ✔ No freezing or crashes
# ✔ Both systems run independently


# ========================================
# 🚀 WHAT PHASE 3 ENABLES
# ========================================

# Now the system becomes:

# ✔ Backend (Heartbeat Engine)
# ✔ Frontend (GUI Viewer)

# This prepares for:

# ➡ Phase 4: Live Auto-Refresh Dashboard
# ➡ Phase 5: System Tray Integration
# ➡ Phase 6: Full Monitoring Application
# ========================================

# ========================================
# 🟡 HEARTBEAT AGENT — PHASE 4 DOCUMENTATION
# LIVE DATA REFRESH SYSTEM (PyQt6)
# ========================================

# 🎯 OBJECTIVE OF PHASE 4
# ----------------------------------------
# Phase 4 upgrades the GUI from a manual log viewer into a LIVE MONITORING DASHBOARD.

# The goal is:

# ✔ Auto-refresh logs every 1 second
# ✔ Display real-time heartbeat updates
# ✔ Remove manual refresh button dependency
# ✔ Keep GUI responsive at all times
# ✔ Ensure Phase 2 heartbeat continues independently

# IMPORTANT:
# - NO while loops in GUI
# - NO time.sleep() in GUI thread
# - Updates must use QTimer (event-driven model)


# ========================================
# 🧠 CORE IDEA OF PHASE 4
# ========================================

# Instead of manual refresh:

#     User clicks button → load logs

# We now use automatic refresh:

#     QTimer → calls load_logs() every 1 second


# This converts the system into:

# REAL-TIME MONITORING DASHBOARD


# ========================================
# 🧱 UPDATED SYSTEM ARCHITECTURE
# ========================================

# PHASE 2 (BACKEND - HEARTBEAT ENGINE)
# ----------------------------------------
# Heartbeat Thread
#         ↓
# Writes logs to:
# logs/data.log


# PHASE 4 (FRONTEND - LIVE DASHBOARD)
# ----------------------------------------
# PyQt6 GUI
#         ↓
# QTimer (every 1 second)
#         ↓
# Reads logs/data.log
#         ↓
# Updates UI automatically


# KEY FLOW:
# Heartbeat → File → GUI Timer → Display


# ========================================
# ⚙️ KEY UPGRADE IN PHASE 4
# ========================================

# PHASE 3 (OLD)
# ----------------------------------------
# ✔ Manual refresh button
# ✔ User triggers log update


# PHASE 4 (NEW)
# ----------------------------------------
# ✔ Automatic updates every 1 second
# ✔ No user interaction required
# ✔ Continuous live feed


# ========================================
# 🧠 IMPORTANT CONCEPTS
# ========================================

# 1. EVENT-DRIVEN UPDATES
# ----------------------------------------
# Instead of loops:

# ❌ while True:
#        load_logs()

# We use:

# ✔ QTimer → triggers function repeatedly


# 2. WHY QTimer IS USED
# ----------------------------------------
# ✔ Non-blocking
# ✔ GUI remains responsive
# ✔ Works inside Qt event loop
# ✔ Safe for single-threaded GUI apps


# 3. GUI THREAD RULE
# ----------------------------------------
# Qt GUI must NEVER be blocked.

# DO NOT:
# ❌ time.sleep()
# ❌ infinite loops
# ❌ heavy processing in main thread


# ========================================
# 🟢 PHASE 4 CODE EXPLANATION
# ========================================

# MAIN COMPONENTS:

# 1. QTextEdit
# ----------------------------------------
# Displays logs in scrollable window


# 2. QTimer
# ----------------------------------------
# Triggers automatic updates every 1000 ms


# 3. load_logs()
# ----------------------------------------
# Reads log file and updates UI


# 4. verticalScrollBar()
# ----------------------------------------
# Auto-scrolls to latest log entry



# ========================================
# 🧪 WHAT YOU WILL OBSERVE
# ========================================

# BEFORE PHASE 4:
# ----------------------------------------
# ✔ Manual refresh required
# ✔ Button click updates logs


# AFTER PHASE 4:
# ----------------------------------------
# ✔ Logs update automatically every 1 second
# ✔ New heartbeat entries appear instantly
# ✔ No button required
# ✔ Smooth scrolling to latest entry
# ✔ UI remains responsive


# Example live output:

# 10:00:00 | HEARTBEAT
# 10:00:05 | HEARTBEAT
# 10:00:10 | HEARTBEAT   ← appears automatically
# 10:00:15 | HEARTBEAT   ← appears automatically


# ========================================
# 🧠 KEY LEARNINGS FROM PHASE 4
# ========================================

# 1. EVENT-DRIVEN PROGRAMMING
# ----------------------------------------
# System reacts to timer events instead of loops.


# 2. REAL-TIME DASHBOARD LOGIC
# ----------------------------------------
# Data flow:

# Heartbeat → File → Timer → GUI → Display


# 3. NON-BLOCKING UI DESIGN
# ----------------------------------------
# ✔ No freezing
# ✔ No infinite loops
# ✔ No sleep in GUI thread


# 4. INDUSTRY PATTERN
# ----------------------------------------
# This is the same model used in:

# ✔ System monitors
# ✔ Task managers
# ✔ Performance dashboards
# ✔ Logging tools


# ========================================
# 🟡 PHASE 4 SUCCESS CRITERIA
# ========================================

# You have completed Phase 4 when:

# ✔ GUI updates automatically every 1 second
# ✔ New logs appear without user input
# ✔ UI remains responsive
# ✔ Scroll stays at latest entry
# ✔ Phase 2 heartbeat continues independently
# ✔ No freezing or lag


# ========================================
# 🚀 WHAT PHASE 4 ENABLES
# ========================================

# Now your system becomes a REAL monitoring dashboard:

# ✔ Backend (Heartbeat Engine)
# ✔ Frontend (Live GUI Dashboard)
# ✔ Auto-refresh system (QTimer)

# NEXT POSSIBLE UPGRADE:

# ➡ Phase 5: System Tray Application
# ➡ Phase 6: Advanced Monitoring Dashboard (filters, charts, alerts)
# ========================================

# Phase 5 introduces System Tray Integration, transforming the Heartbeat Agent from a standard desktop application into a background desktop agent.

# In previous phases:

# Phase 2 introduced a background heartbeat thread.
# Phase 3 introduced a log visualization interface.
# Phase 4 introduced automatic live log refreshing.

# Phase 5 adds operating system integration through a system tray icon, allowing the application to run in the background while remaining accessible through the system tray.

# This design pattern is commonly used by applications such as:

# Discord
# Telegram Desktop
# Microsoft OneDrive
# Dropbox
# Antivirus Software
# Monitoring and Diagnostic Tools

# The heartbeat engine continuously writes data.

# The GUI continuously reads data.

# The system tray provides user access and control.

# Component	Purpose
# QSystemTrayIcon	     Creates tray icon
# QMenu                	 Creates tray context menu
# QAction	             Creates menu actions
# QIcon	                 Loads custom icons
# isNull()	             Validates icon loading
# toggle_window()	     Shows/Hides window
# tray_clicked()	     Handles tray interactions
# exit_app()	         Exits application


# QSystemTrayIcon
# Import
# from PyQt6.QtWidgets import QSystemTrayIcon
# Purpose

# Creates an icon inside the operating system's system tray.

# Creation
# self.tray = QSystemTrayIcon(self)
# Responsibilities
# Displays tray icon
# Receives tray events
# Opens tray menu
# Provides application access while hidden
# Benefits

# Without a tray icon:

# Application
#     ↓
# Window Required

# With a tray icon:

# Application
#     ↓
# Runs In Background
#     ↓
# Accessible From Tray
# Custom Tray Icon System
# Purpose

# Allows the application to use a custom icon instead of a default Qt icon.

# get_app_icon()
# Function
# def get_app_icon(self):
# Purpose

# Loads a custom icon from the assets directory.

# Implementation
# def get_app_icon(self):
#     icon_path = "assets/app_icon.png"

#     icon = QIcon(icon_path)

#     if not icon.isNull():
#         return icon

#     return QApplication.style().standardIcon(
#         QApplication.style().StandardPixmap.SP_ComputerIcon
#     )
# Icon File Location

# Expected project structure:

# project/
# │
# ├── assets/
# │   └── app_icon.png
# │
# ├── logs/
# │   └── data.log
# │
# └── main.py
# QIcon
# Import
# from PyQt6.QtGui import QIcon
# Purpose

# Represents an icon object used by Qt.

# Creation
# icon = QIcon("assets/app_icon.png")
# Supported Formats
# PNG
# ICO
# JPG
# SVG
# Uses
# Tray icons
# Window icons
# Toolbar icons
# Menu icons
# isNull()
# Method
# icon.isNull()
# Purpose

# Determines whether an icon loaded successfully.

# Returns
# True
#     Icon failed to load

# False
#     Icon loaded successfully
# Why It Is Used

# Without validation:

# QIcon("missing_icon.png")

# may silently fail.

# The validation step ensures the application always has an icon available.

# Fallback Icon System

# If the custom icon cannot be loaded:

# return QApplication.style().standardIcon(
#     QApplication.style().StandardPixmap.SP_ComputerIcon
# )

# Qt automatically provides a built-in icon.

# Workflow
# Custom Icon Found?
#         │
#  ┌──────┴──────┐
#  │             │
# YES           NO
#  │             │
#  ▼             ▼
# Use PNG   Use Qt Default Icon
# Benefits
# Prevents missing tray icons
# Prevents crashes
# Provides graceful fallback behavior
# Setting Tray Icon
# Code
# self.tray.setIcon(
#     self.get_app_icon()
# )
# Purpose

# Assigns the selected icon to the tray.

# Workflow
# Load Icon
#     │
#     ▼
# Validate Icon
#     │
#     ▼
# Set Tray Icon
# QMenu
# Import
# from PyQt6.QtWidgets import QMenu
# Purpose

# Creates a context menu displayed when the user right-clicks the tray icon.

# Creation
# menu = QMenu(self)
# QAction
# Import
# from PyQt6.QtGui import QAction
# Purpose

# Represents clickable menu commands.

# Creation
# self.toggle_action = QAction(
#     "Show Window",
#     self
# )

# self.quit_action = QAction(
#     "Exit",
#     self
# )
# Current Actions
# Action	Purpose
# Show Window	Open dashboard
# Exit	Close application
# Connecting Actions
# Code
# self.toggle_action.triggered.connect(
#     self.toggle_window
# )

# self.quit_action.triggered.connect(
#     self.exit_app
# )
# Purpose

# Connects menu actions to application functions.

# Flow
# User Clicks Menu Item
#           │
#           ▼
# triggered Signal
#           │
#           ▼
# Connected Function Runs
# Adding Actions To Menu
# Code
# menu.addAction(self.toggle_action)
# menu.addAction(self.quit_action)
# Purpose

# Adds actions to the tray menu.

# Assigning Menu To Tray
# Code
# self.tray.setContextMenu(menu)
# Purpose

# Associates the menu with the tray icon.

# Result

# Right-clicking the tray icon displays the menu.

# Tray Event Handling
# Code
# self.tray.activated.connect(
#     self.tray_clicked
# )
# Purpose

# Detects interactions with the tray icon.

# tray_clicked()
# Function
# def tray_clicked(self, reason):
# Purpose

# Processes tray activation events.

# ActivationReason.DoubleClick
# Code
# if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
# Purpose

# Detects double-click events.

# Workflow
# Double Click Tray Icon
#           │
#           ▼
# toggle_window()
# Window Toggle System
# Function
# def toggle_window(self):
# Purpose

# Shows or hides the dashboard window.

# Show Window
# Methods
# self.show()
# self.raise_()
# self.activateWindow()
# Explanation
# show()

# Displays the window.

# raise_()

# Brings the window above other windows.

# activateWindow()

# Gives focus to the window.

# Hide Window
# Method
# self.hide()
# Purpose

# Removes the window from view without closing the application.

# Dynamic Menu Text
# Show State
# self.toggle_action.setText(
#     "Show Window"
# )
# Hide State
# self.toggle_action.setText(
#     "Hide Window"
# )
# Benefit

# Menu text always reflects the current state.

# Tray Startup Behavior
# Code
# self.tray.show()
# self.hide()
# Purpose

# Starts application in background mode.

# Result
# Application Starts
#         │
#         ▼
# Tray Icon Appears
#         │
#         ▼
# Window Remains Hidden
# Live Refresh Integration

# Phase 5 retains the Phase 4 refresh system.

# Code
# self.timer = QTimer()

# self.timer.timeout.connect(
#     self.load_logs
# )

# self.timer.start(1000)
# Purpose

# Updates displayed logs every second.

# Benefits
# No refresh button needed
# Dashboard updates automatically
# Monitoring feels real-time
# Application Exit
# Function
# def exit_app(self):
# Current Implementation
# QApplication.quit()
# Recommended Version
# def exit_app(self):
#     self.tray.hide()
#     QApplication.quit()
# Benefits
# Clean shutdown
# Removes tray icon
# Prevents ghost icons