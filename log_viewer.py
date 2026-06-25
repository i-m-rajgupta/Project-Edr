import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton

LOG_FILE = Path("logs/data.log")

class LogViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Heartbeat Log Viewer")
        self.setGeometry(300,200,700,500)

        layout = QVBoxLayout()

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        self.refresh_button = QPushButton("Load Logs")
        self.refresh_button.clicked.connect(self.load_logs)

        layout.addWidget(self.log_area)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)

        self.load_logs()

    def load_logs(self):
        if LOG_FILE.exists():
            try:
                with open(LOG_FILE,"r",encoding="utf-8") as file:
                    content = file.read()

                self.log_area.setText(content)

            except Exception as e:
                self.log_area.setText(f"Error reading log file : {e}")

        else:
            self.log_area.setText("Log file not found.") 

def main():
    app = QApplication(sys.argv)

    window = LogViewer()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()                               

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