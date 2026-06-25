import winshell
from win32com.client import Dispatch
import os
from pathlib import Path

startup = winshell.startup()
target = Path(os.getenv("LOCALAPPDATA")) / "EdrAgent" / "EdrAgent.exe"

shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(str(Path(startup) / "EdrAgent.lnk"))
shortcut.TargetPath = str(target)
shortcut.WorkingDirectory = str(target.parent)
shortcut.save()

# This script creates a Windows Startup shortcut (.lnk file) that automatically launches the EdrAgent.exe application when the user logs into Windows.

# It is part of a Phase 8 deployment system, where the application becomes installable and persistent.

# 📌 Purpose
# Enable auto-start on login
# Avoid manual execution of the application
# Implement basic persistence mechanism
# Integrate installed application with Windows Startup folder
# 🧠 Full Script
# import os
# from pathlib import Path
# from win32com.client import Dispatch

# startup = Path(os.environ["APPDATA"]) / r"Microsoft\Windows\Start Menu\Programs\Startup"

# target = Path(os.environ["LOCALAPPDATA"]) / "EdrAgent" / "EdrAgent.exe"

# shortcut_path = startup / "EdrAgent.lnk"

# shell = Dispatch("WScript.Shell")
# shortcut = shell.CreateShortCut(str(shortcut_path))
# shortcut.TargetPath = str(target)
# shortcut.WorkingDirectory = str(target.parent)
# shortcut.save()

# print("Startup shortcut created")
# 🔍 Line-by-Line Explanation
# 1. Import OS module
# import os

# Used to access system environment variables such as:

# APPDATA
# LOCALAPPDATA

# These variables point to user-specific Windows directories.

# 2. Import Path handler
# from pathlib import Path

# Provides a modern and safe way to handle file paths.

# Benefits:

# OS-independent path handling
# Cleaner syntax than string concatenation
# Reduces path-related errors
# 3. Import Windows COM interface
# from win32com.client import Dispatch

# Allows Python to interact with Windows COM objects.

# Used here to access:

# WScript.Shell (Windows shortcut creator)
# 📂 4. Locate Startup folder
# startup = Path(os.environ["APPDATA"]) / r"Microsoft\Windows\Start Menu\Programs\Startup"
# Description:

# Retrieves the current user's Startup folder location.

# Example path:
# C:\Users\<User>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
# Purpose:

# Any .lnk file placed here will execute automatically at login.

# 📦 5. Define application path
# target = Path(os.environ["LOCALAPPDATA"]) / "EdrAgent" / "EdrAgent.exe"
# Description:

# Defines the installed application executable location.

# Example path:
# C:\Users\<User>\AppData\Local\EdrAgent\EdrAgent.exe
# Purpose:

# This is the program that will run at startup.

# 🔗 6. Define shortcut file path
# shortcut_path = startup / "EdrAgent.lnk"
# Description:

# Creates the shortcut file name inside Startup folder.

# Result:
# EdrAgent.lnk
# 🧩 7. Create Windows Shell object
# shell = Dispatch("WScript.Shell")
# Description:

# Creates a Windows Shell COM interface.

# Purpose:

# Used to generate .lnk shortcut files using Windows-native APIs.

# 📎 8. Create shortcut object
# shortcut = shell.CreateShortCut(str(shortcut_path))
# Description:

# Initializes a shortcut file at the given location.

# Note:

# Path is converted to string because COM API requires string input.

# 🎯 9. Set shortcut target
# shortcut.TargetPath = str(target)
# Description:

# Defines the executable that will be launched.

# 📁 10. Set working directory
# shortcut.WorkingDirectory = str(target.parent)
# Description:

# Sets the folder from which the application will run.

# Purpose:

# Ensures:

# correct relative file access
# proper log/config loading
# 💾 11. Save shortcut
# shortcut.save()
# Description:

# Writes the .lnk file to disk in the Startup folder.

# 📢 12. Confirmation message
# print("Startup shortcut created")
# Description:

# Prints success message after shortcut creation.

# 🔄 Execution Flow
# Script runs
#    ↓
# Locate Startup folder
#    ↓
# Find installed EdrAgent.exe
#    ↓
# Create .lnk shortcut
#    ↓
# Save shortcut in Startup folder
#    ↓
# Windows executes app on login
# ⚠️ Notes
# Requires pywin32 package
# Works only on Windows OS
# User must have application installed in LOCALAPPDATA path
# No administrator privileges required
# 🧪 Output

# After execution:

# C:\Users\<User>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\EdrAgent.lnk
# 📌 Summary

# This script implements a user-level persistence mechanism by leveraging the Windows Startup folder and COM-based shortcut creation.

# It is commonly used in:

# desktop applications
# tray utilities
# background agents