import winreg

# To add startup key in registry

exe_path = r"A:\Project AC\Dummy Edr\dist\EdrAgent.exe"

key = winreg.OpenKey(
    winreg.HKEY_CURRENT_USER,
    r"Software\Microsoft\Windows\CurrentVersion\Run",
    0,
    winreg.KEY_SET_VALUE
)



winreg.SetValueEx(
    key,
    "EdrAgent",
    0,
    winreg.REG_SZ,
    exe_path
)

winreg.CloseKey(key)

print("Startup key added")

# For deleting the entry
# key = winreg.OpenKey(
#     winreg.HKEY_CURRENT_USER,
#     r"Software\Microsoft\Windows\CurrentVersion\Run",
#     0,
#     winreg.KEY_SET_VALUE
# )

# winreg.DeleteValue(key, "EdrAgent")
# winreg.CloseKey(key)
# print("Startup key deleted successfully !!")

# This script uses Python's built-in winreg module to interact with the Windows Registry. Specifically, it adds an entry to the Startup (Run) registry key, so that a program starts automatically whenever the current user logs into Windows.

# To understand the code, it's important to first understand the Windows Registry.

# What is the Windows Registry?

# The Windows Registry is a hierarchical database that stores:

# Windows configuration settings
# Installed software information
# Hardware settings
# User preferences
# Startup programs

# Think of it as a huge configuration database.

# It contains several top-level sections called Registry Hives.

# Some common hives are:

# HKEY_CLASSES_ROOT (HKCR)
# HKEY_CURRENT_USER (HKCU)
# HKEY_LOCAL_MACHINE (HKLM)
# HKEY_USERS (HKU)
# HKEY_CURRENT_CONFIG (HKCC)

# Your program uses:

# HKEY_CURRENT_USER

# which stores settings only for the currently logged-in user.

# What is the Run Key?

# Inside the registry is the following location:

# HKEY_CURRENT_USER
#     └── Software
#           └── Microsoft
#                 └── Windows
#                       └── CurrentVersion
#                             └── Run

# Anything stored inside the Run key is executed automatically when the user logs in.

# Example:

# Run

# ChromeUpdater     C:\Program Files\Chrome\update.exe
# Spotify           C:\Spotify\Spotify.exe
# OneDrive          C:\Users\User\AppData\Local\Microsoft\OneDrive.exe

# If your program adds

# EdrAgent
# A:\Project AC\Dummy Edr\dist\EdrAgent.exe

# Windows automatically launches

# EdrAgent.exe

# at every login.

# Understanding the winreg Module

# Python provides a built-in module called

# import winreg

# This module allows Python programs to

# Create registry keys
# Open registry keys
# Read registry values
# Modify registry values
# Delete registry values

# without manually using the Registry Editor (regedit.exe).

# Code Explanation (Line by Line)
# Line 1
# import winreg

# Imports Python's Registry API.

# After importing it, you can perform operations on the Windows Registry.

# Comment
# # To add startup key in registry

# This is just a comment explaining the purpose.

# Line
# exe_path = r"A:\Project AC\Dummy Edr\dist\EdrAgent.exe"

# Stores the full path of the executable.

# Notice the r before the string.

# r"..."

# means

# Raw String

# Normally,

# "C:\new\test"

# would treat

# \n

# as a newline.

# A raw string prevents this.

# Example

# Without raw string:

# "C:\new"

# becomes

# C:
# ew

# With raw string

# r"C:\new"

# Python stores exactly

# C:\new
# Opening the Registry Key
# key = winreg.OpenKey(

# This opens an existing registry key.

# Think of it like opening a file before editing it.

# First Parameter
# winreg.HKEY_CURRENT_USER

# This is the registry hive.

# Equivalent to

# HKCU
# Second Parameter
# r"Software\Microsoft\Windows\CurrentVersion\Run"

# This is the path inside HKCU.

# So Python opens

# HKCU
#     Software
#         Microsoft
#             Windows
#                 CurrentVersion
#                     Run
# Third Parameter
# 0

# This is the reserved value.

# Windows requires it.

# Almost always

# 0
# Fourth Parameter
# winreg.KEY_SET_VALUE

# This specifies what permissions you need.

# Possible permissions include:

# KEY_READ

# Only read values.

# KEY_WRITE

# Write values.

# KEY_SET_VALUE

# Modify values only.

# KEY_ALL_ACCESS

# Everything.

# Since the program only writes,

# KEY_SET_VALUE

# is enough.

# After this,

# key

# contains a handle to the Run registry key.

# Think of it like

# file = open(...)

# but for the registry.

# Adding the Startup Entry
# winreg.SetValueEx(

# This function creates or updates a registry value.

# Its syntax is:

# SetValueEx(
#     key,
#     value_name,
#     reserved,
#     type,
#     data
# )

# Let's explain each argument.

# Argument 1
# key

# The registry key that was opened earlier.

# Equivalent to

# HKCU\Software\Microsoft\Windows\CurrentVersion\Run
# Argument 2
# "EdrAgent"

# The name of the registry value.

# In Registry Editor you'll see

# Name        Data

# EdrAgent    A:\Project AC\Dummy Edr\dist\EdrAgent.exe

# The name can be anything.

# Example

# Updater

# MyProgram

# StartupService

# Chrome

# Spotify
# Argument 3
# 0

# Reserved.

# Always

# 0
# Argument 4
# winreg.REG_SZ

# Specifies the data type.

# Some registry data types are:

# REG_SZ

# String

# REG_DWORD

# 32-bit integer

# REG_BINARY

# Binary data

# REG_MULTI_SZ

# Multiple strings

# REG_QWORD

# 64-bit integer

# Since an executable path is text,

# REG_SZ

# is appropriate.

# Argument 5
# exe_path

# The actual data stored.

# Which equals

# A:\Project AC\Dummy Edr\dist\EdrAgent.exe

# Windows later reads this string and launches that executable during login.

# Closing the Registry
# winreg.CloseKey(key)

# Closes the registry handle.

# Just like

# file.close()

# after working with a file.

# This releases the system resource.

# Printing Success
# print("Startup key added")

# Displays

# Startup key added

# This only confirms that the script completed without raising an exception.

# Deleting the Startup Entry

# The commented-out section removes the registry value instead of creating it.

# Open the registry again

# key = winreg.OpenKey(

# This opens the same

# Run

# key.

# Delete the value

# winreg.DeleteValue(key, "EdrAgent")

# This removes

# Name : EdrAgent

# from the registry.

# After deletion

# Before:

# Run

# EdrAgent
# Chrome
# Spotify

# After:

# Run

# Chrome
# Spotify

# Now Windows will no longer launch EdrAgent.exe at login.

# Close the key

# winreg.CloseKey(key)

# Releases the registry handle.

# Print confirmation

# print("Startup key deleted successfully !!")

# Displays

# Startup key deleted successfully !!
# How the Entire Process Works

# The workflow can be visualized as:

# Python Script
#       │
#       ▼
# Import winreg
#       │
#       ▼
# Open HKCU\Software\Microsoft\Windows\CurrentVersion\Run
#       │
#       ▼
# Create Registry Value
#       │
#       ▼
# Name  : EdrAgent
# Data  : A:\Project AC\Dummy Edr\dist\EdrAgent.exe
#       │
#       ▼
# Close Registry
#       │
#       ▼
# User Logs Into Windows
#       │
#       ▼
# Windows Reads Run Key
#       │
#       ▼
# Launches
# EdrAgent.exe
# Example of the Registry After Running the Script

# If you open the Registry Editor (regedit) and navigate to:

# HKEY_CURRENT_USER
#     Software
#         Microsoft
#             Windows
#                 CurrentVersion
#                     Run

# you would see something like:

# Name	Type	Data
# EdrAgent	REG_SZ	A:\Project AC\Dummy Edr\dist\EdrAgent.exe

# At the next login, Windows reads this value and starts the executable automatically.

# Why This Is Commonly Used

# Registering a program under the Run key is a standard Windows mechanism for launching applications automatically after a user signs in. Many legitimate applications use it for background services or update checkers. It's also important to understand from a defensive perspective because security software often monitors these startup locations—programs that add themselves to startup without the user's knowledge can be flagged for review since persistence mechanisms are commonly used by both legitimate software and malware.