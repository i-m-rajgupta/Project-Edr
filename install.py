import os
import shutil
from pathlib import Path

APP_NAME = "EdrAgent.exe"

local_appdata = os.getenv("LOCALAPPDATA")
program_data = os.getenv("PROGRAMDATA")

install_dir = Path(local_appdata) / "EdrAgent"
data_dir = Path(program_data) / "EdrAgent" / "logs"

install_dir.mkdir(parents=True, exist_ok=True)
data_dir.mkdir(parents=True, exist_ok=True)

# Copy EXE
source_exe = Path("dist") / APP_NAME
target_exe = install_dir / APP_NAME

shutil.copy2(source_exe, target_exe)

print("Installed at:", target_exe)
print("Logs at:", data_dir)

# =========================================================
# PHASE 8 — INSTALLATION, PACKAGING & PERSISTENCE
# =========================================================

# PROJECT:
# Heartbeat Agent / Desktop Monitoring Agent

# PHASE OBJECTIVE
# ---------------------------------------------------------

# Previous phases focused on building the application:

# Phase 1  → Logging System
# Phase 2  → Background Thread
# Phase 3  → GUI Viewer
# Phase 4  → Live Refresh
# Phase 5  → System Tray
# Phase 6  → Unified Architecture
# Phase 7  → Daemon-Style Behavior

# Phase 8 focuses on deployment.

# The application is no longer just a Python project.

# It becomes:

#     Installable
#     Runnable outside development environment
#     Persistent across logins
#     Closer to real desktop agent software

# =========================================================
# PHASE 8 OVERVIEW
# =========================================================

# Phase 8 introduces three major concepts:

# 1. Application Packaging
# 2. Installation
# 3. Persistence (Auto Start)

# Architecture:

# Developer Machine
#         │
#         ▼
# PyInstaller Build
#         │
#         ▼
# HeartbeatAgent.exe
#         │
#         ▼
# Install to LocalAppData
#         │
#         ▼
# Auto Start at Login
#         │
#         ▼
# Background Agent Starts Automatically

# =========================================================
# SECTION 1 — APPLICATION PACKAGING
# =========================================================

# WHAT IS PACKAGING?
# ---------------------------------------------------------

# Python applications normally require:

# - Python interpreter
# - Source code
# - Installed dependencies

# Example:

# app.py
# heartbeat.py
# tray_controller.py
# log_viewer.py

# To run:

# python app.py

# This is not suitable for end users.

# Users should be able to run:

# HeartbeatAgent.exe

# without installing Python.

# Packaging solves this problem.

# =========================================================
# PYINSTALLER
# =========================================================

# PyInstaller converts:

# Python Source Code
#         ↓
# Standalone Windows Executable

# Example:

# app.py
#         ↓
# PyInstaller
#         ↓
# HeartbeatAgent.exe

# The generated executable contains:

# - Python runtime
# - Project code
# - Required libraries
# - Application entry point

# Users do not need Python installed.

# =========================================================
# INSTALLING PYINSTALLER
# =========================================================

# Install:

# pip install pyinstaller

# Verify:

# pyinstaller --version

# =========================================================
# CREATING THE EXE
# =========================================================

# Basic build:

# pyinstaller --onefile app.py

# Output:

# dist/
#     app.exe

# build/
#     ...

# app.spec

# Important folders:

# dist/
#     Final executable

# build/
#     Temporary build files

# .spec
#     Build configuration

# =========================================================
# USEFUL PYINSTALLER OPTIONS
# =========================================================

# 1. Single File

# --onefile

# Example:

# pyinstaller --onefile app.py

# Result:

# One executable file.

# ---------------------------------------------------------

# 2. No Console Window

# --noconsole

# Example:

# pyinstaller --onefile --noconsole app.py

# Useful for tray applications.

# Without:

# Black terminal appears.

# With:

# Only tray icon appears.

# ---------------------------------------------------------

# 3. Custom Icon

# --icon=assets/app_icon.ico

# Example:

# pyinstaller --onefile --noconsole ^
#     --icon=assets/app_icon.ico ^
#     app.py

# Result:

# Custom Windows executable icon.

# ---------------------------------------------------------

# 4. Application Name

# --name HeartbeatAgent

# Example:

# pyinstaller --onefile ^
#     --name HeartbeatAgent ^
#     app.py

# Output:

# HeartbeatAgent.exe

# =========================================================
# FINAL BUILD COMMAND
# =========================================================

# Example:

# pyinstaller ^
#     --onefile ^
#     --noconsole ^
#     --name HeartbeatAgent ^
#     --icon assets/app_icon.ico ^
#     app.py

# Output:

# dist/
#     HeartbeatAgent.exe

# =========================================================
# INCLUDING ADDITIONAL FILES
# =========================================================

# Problem:

# PyInstaller only bundles Python code.

# Files such as:

# assets/app_icon.png

# may not be found.

# Solution:

# --add-data

# Example:

# pyinstaller ^
#     --onefile ^
#     --noconsole ^
#     --add-data "assets;assets" ^
#     app.py

# This copies assets into the executable package.

# =========================================================
# TESTING THE EXE
# =========================================================

# Before installation verify:

# 1. EXE launches
# 2. Tray icon appears
# 3. GUI opens
# 4. Heartbeat runs
# 5. Logs are written
# 6. No crashes occur

# =========================================================
# SECTION 2 — APPLICATION INSTALLATION
# =========================================================

# WHY INSTALL?
# ---------------------------------------------------------

# Without installation:

# Project Folder
#     └── dist/HeartbeatAgent.exe

# User must manually locate and launch it.

# Installation creates:

# Permanent application location
# Standard file structure
# Future upgrade path

# =========================================================
# INSTALL LOCATION
# =========================================================

# Initial attempt:

# C:\Program Files\EdrAgent

# Problem:

# Windows requires administrator permissions.

# Error:

# PermissionError:
# WinError 5
# Access is denied

# =========================================================
# LOCALAPPDATA INSTALLATION
# =========================================================

# Solution:

# Install into user space.

# Location:

# %LOCALAPPDATA%\EdrAgent

# Example:

# C:\Users\<User>\AppData\Local\EdrAgent

# Benefits:

# No administrator rights required
# Easy development
# Easy testing
# Safe installation location

# =========================================================
# INSTALLER SCRIPT
# =========================================================

# Example structure:

# Source:

# dist/HeartbeatAgent.exe

# Target:

# LOCALAPPDATA\EdrAgent\HeartbeatAgent.exe

# Installer responsibilities:

# 1. Create install folder
# 2. Copy executable
# 3. Verify installation

# Example flow:

# Installer
#         ↓
# Create Folder
#         ↓
# Copy EXE
#         ↓
# Installation Complete

# =========================================================
# APPLICATION DATA STORAGE
# =========================================================

# Separate application files from application data.

# Application Files:

# LOCALAPPDATA\EdrAgent

# Contains:

# HeartbeatAgent.exe

# Application Data:

# PROGRAMDATA\EdrAgent

# Contains:

# logs/
#     data.log

# =========================================================
# WHY SEPARATE THEM?
# =========================================================

# Application Files

# Purpose:

# Executable code

# Examples:

# HeartbeatAgent.exe
# assets
# configuration

# ---------------------------------------------------------

# Application Data

# Purpose:

# Persistent runtime information

# Examples:

# Logs
# Telemetry
# Databases
# Settings

# This follows common Windows software practices.

# =========================================================
# SECTION 3 — PERSISTENCE
# =========================================================

# WHAT IS PERSISTENCE?
# ---------------------------------------------------------

# Persistence means:

# Application starts automatically.

# Without persistence:

# User logs in
#         ↓
# Must manually start application

# With persistence:

# User logs in
#         ↓
# Application starts automatically

# =========================================================
# STARTUP FOLDER PERSISTENCE
# =========================================================

# Windows provides:

# Startup Folder

# Open:

# Win + R

# Type:

# shell:startup

# Location:

# User Startup Folder

# Anything placed here launches automatically at login.

# =========================================================
# IMPLEMENTATION
# =========================================================

# Create shortcut:

# HeartbeatAgent.exe
#         ↓
# Shortcut
#         ↓
# Startup Folder

# Result:

# Login
#         ↓
# Heartbeat Agent Starts
#         ↓
# Tray Appears
#         ↓
# Heartbeat Runs

# =========================================================
# PERSISTENCE TEST
# =========================================================

# Verify:

# 1. Install application
# 2. Add shortcut to Startup Folder
# 3. Log out
# 4. Log back in

# Expected:

# ✔ Tray icon appears
# ✔ Heartbeat starts
# ✔ Logs continue updating
# ✔ No manual launch required

# =========================================================
# FULL PHASE 8 ARCHITECTURE
# =========================================================

# User Login
#         │
#         ▼
# Startup Folder
#         │
#         ▼
# HeartbeatAgent.exe
#         │
#         ▼
# Agent Controller
#         │
#  ┌──────┼────────┐
#  │      │        │
#  ▼      ▼        ▼

# Engine  Tray    GUI
#         │
#         ▼
# ProgramData Logs

# =========================================================
# WHAT PHASE 8 TAUGHT
# =========================================================

# 1. Packaging
# ---------------------------------------------------------

# How Python applications become standalone executables.

# Tools:

# - PyInstaller

# Concepts:

# - One-file executable
# - Embedded Python runtime
# - Asset packaging

# ---------------------------------------------------------

# 2. Installation
# ---------------------------------------------------------

# How applications are deployed.

# Concepts:

# - Installation directory
# - Application files
# - Application data

# Locations:

# - LOCALAPPDATA
# - PROGRAMDATA

# ---------------------------------------------------------

# 3. Persistence
# ---------------------------------------------------------

# How applications automatically start.

# Concepts:

# - Startup Folder
# - Login persistence
# - Background execution

# ---------------------------------------------------------

# 4. Real Application Lifecycle
# ---------------------------------------------------------

# Development Project
#         ↓
# Packaged Executable
#         ↓
# Installed Application
#         ↓
# Persistent Background Agent

# =========================================================
# PHASE 8 SUCCESS CHECKLIST
# =========================================================

# ✔ PyInstaller installed
# ✔ EXE successfully generated
# ✔ Custom application name configured
# ✔ Optional icon configured
# ✔ Application runs without Python installed
# ✔ Installer copies EXE to LOCALAPPDATA
# ✔ Logs stored in PROGRAMDATA
# ✔ Startup Folder persistence configured
# ✔ Application starts automatically at login
# ✔ Tray icon appears automatically
# ✔ Heartbeat continues running
# ✔ GUI opens on demand
# ✔ Application works independently of development folder

# =========================================================
# END OF PHASE 8
# =========================================================

# Current Status:

# ✔ Packaged Desktop Agent
# ✔ Installed Application
# ✔ Login Persistence
# ✔ Background Execution
# ✔ System Tray Control
# ✔ On-Demand GUI

# Next Logical Phase:

# PHASE 9 — Uninstallation & Cleanup

# Goals:

# - Remove installed files
# - Remove startup persistence
# - Remove logs (optional)
# - Clean application lifecycle management

# The project now behaves much closer to a real desktop monitoring agent than a standalone Python application.