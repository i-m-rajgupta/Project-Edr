from datetime import datetime
import time
from pathlib import Path

LOG_DIR = Path("logs")

LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "data.log"
INTERVAL = 5

def write_heartbeat():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = f"{timestamp} | HEARTBEAT | System is running \n"
    
    try:
        with open(LOG_FILE,"a",encoding="utf-8") as file:
            file.write(entry)

        print(entry.strip())
    
    except OSError as e:
        print(f"[ERROR] Failed to write log: {e}")
def main():
    print("Heartbeat Agent Started...")

    try:
        while True:
            write_heartbeat()
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        shutdown_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(LOG_FILE, "a", encoding="utf-8") as file:
                file.write(
                    f"{shutdown_time} | SYSTEM | Agent stopped by user\n"
                )
        except OSError:
            pass

        print("\nHeartbeat Agent Stopped.")

    except Exception as e:
        print(f"\n[CRITICAL ERROR] {e}")

if __name__ == "__main__":
    main()

# HEARTBEAT AGENT - PROJECT DOCUMENTATION

# The Heartbeat Agent is a Python-based monitoring utility that periodically records heartbeat messages to a log file. A heartbeat is a status message generated at regular intervals to indicate that a process or application is functioning correctly.

# This application writes a heartbeat entry every 5 seconds, stores the entry in a log file, and displays the message on the console. It also includes error handling, automatic log directory creation, and graceful shutdown functionality.

# The purpose of this application is to:

# • Monitor process availability.
# • Demonstrate file handling in Python.
# • Record timestamped system events.
# • Create a foundation for health-check systems.
# • Practice exception handling and logging techniques.

# datetime

# from datetime import datetime

# Purpose:
# Retrieves the current date and time for heartbeat timestamps.

# Example:

# datetime.now()

# time

# import time

# Purpose:
# Suspends program execution between heartbeat events.

# Example:

# time.sleep(5)

# pathlib

# from pathlib import Path

# Purpose:
# Provides an object-oriented way of working with file and directory paths.

# Advantages:

# • Platform independent.
# • Cleaner syntax.
# • Better readability.
# • Automatic path handling for Windows, Linux, and macOS.

# LOG_DIR = Path("logs")
# LOG_DIR.mkdir(parents=True, exist_ok=True)

# Purpose:

# Creates a directory named "logs" automatically.

# Parameters:

# parents=True
# Creates parent directories if required.

# exist_ok=True
# Prevents errors if the directory already exists.

# Resulting structure:

# project/
# │
# ├── heartbeat.py
# │
# └── logs/
# └── data.log

# LOG_FILE = LOG_DIR / "data.log"

# Purpose:

# Creates the log file path using pathlib.

# Result:

# logs/data.log

# INTERVAL = 5

# Purpose:

# Defines the heartbeat interval in seconds.

# Value:

# 5 seconds

# Purpose:

# Creates and records a heartbeat event.

# STEP 1: Generate Timestamp

# timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Example Output:

# 2026-06-25 15:30:45

# Formatting:

# %Y = Year
# %m = Month
# %d = Day
# %H = Hour
# %M = Minute
# %S = Second

# STEP 2: Create Log Entry

# entry = f"{timestamp} | HEARTBEAT | System is running\n"

# Example:

# 2026-06-25 15:30:45 | HEARTBEAT | System is running

# STEP 3: Write Entry to File

# with open(LOG_FILE, "a", encoding="utf-8") as file:
# file.write(entry)

# Mode:

# "a" = Append Mode

# Behavior:

# • Creates file if missing.
# • Preserves existing log entries.
# • Adds new entries to the end.

# STEP 4: Display Entry

# print(entry.strip())

# Purpose:

# Displays the heartbeat message on the console.

# strip() removes the trailing newline character.

# try:
# ...
# except OSError as e:
# print(f"[ERROR] Failed to write log: {e}")

# Purpose:

# Handles file-related errors such as:

# • Missing permissions.
# • Disk write failures.
# • Invalid paths.
# • Storage issues.

# Example Output:

# [ERROR] Failed to write log: Permission denied

# This prevents the application from crashing during logging operations.

# Purpose:

# Acts as the primary control function of the application.

# print("Heartbeat Agent Started...")

# Console Output:

# Heartbeat Agent Started...

# while True:
# write_heartbeat()
# time.sleep(INTERVAL)

# Purpose:

# Runs indefinitely until interrupted.

# Execution Flow:

# Generate heartbeat.
# Write heartbeat to file.
# Print heartbeat.
# Wait 5 seconds.
# Repeat.

# except KeyboardInterrupt:

# Purpose:

# Handles user termination via:

# CTRL + C

# instead of crashing abruptly.

# SHUTDOWN TIMESTAMP

# shutdown_time = datetime.now().strftime(
# "%Y-%m-%d %H:%M:%S"
# )

# Records the exact shutdown time.

# SHUTDOWN LOG ENTRY

# f"{shutdown_time} | SYSTEM | Agent stopped by user\n"

# Example:

# 2026-06-25 16:45:22 | SYSTEM | Agent stopped by user

# This entry is appended to the log file before exiting.

# CONSOLE OUTPUT

# Heartbeat Agent Stopped.

# Purpose:

# Provides confirmation that the application ended normally.

# try:
# ...
# except OSError:
# pass

# Purpose:

# If logging the shutdown event fails, the program exits gracefully without displaying additional errors.

# except Exception as e:
# print(f"\n[CRITICAL ERROR] {e}")

# Purpose:

# Captures unexpected runtime errors.

# Examples:

# • Programming errors
# • Resource failures
# • Unexpected exceptions

# Example Output:

# [CRITICAL ERROR] Unexpected issue occurred

# This improves application stability and troubleshooting.

# if name == "main":
# main()

# Purpose:

# Ensures the application runs only when executed directly.

# When executed:

# python heartbeat.py

# Result:

# main() starts automatically.

# When imported:

# import heartbeat

# Result:

# Functions become available but the application does not start.

# 2026-06-25 15:30:00 | HEARTBEAT | System is running
# 2026-06-25 15:30:05 | HEARTBEAT | System is running
# 2026-06-25 15:30:10 | HEARTBEAT | System is running
# 2026-06-25 15:30:15 | HEARTBEAT | System is running
# 2026-06-25 15:30:20 | HEARTBEAT | System is running
# 2026-06-25 15:30:25 | SYSTEM | Agent stopped by user

# Program Starts
# │
# ▼
# Import Required Modules
# │
# ▼
# Create logs Directory
# │
# ▼
# Initialize Constants
# │
# ▼
# Execute main()
# │
# ▼
# Display Startup Message
# │
# ▼
# Start Infinite Loop
# │
# ├─ Generate Timestamp
# │
# ├─ Create Heartbeat Entry
# │
# ├─ Write Entry to Log File
# │
# ├─ Display Entry
# │
# ├─ Wait 5 Seconds
# │
# └─ Repeat
# │
# ▼
# CTRL + C Pressed
# │
# ▼
# Record Shutdown Event
# │
# ▼
# Display Shutdown Message
# │
# ▼
# Program Ends

# ✓ Automatic log directory creation

# ✓ Timestamped heartbeat entries

# ✓ Console output monitoring

# ✓ UTF-8 file support

# ✓ Cross-platform path handling

# ✓ Graceful shutdown logging

# ✓ File I/O error handling

# ✓ Unexpected exception handling

# ✓ Infinite heartbeat monitoring

# ✓ Clean and maintainable structure

# The Heartbeat Agent is a lightweight monitoring utility that demonstrates practical use of Python file handling, exception management, process monitoring, and structured logging. Its improved implementation provides greater reliability through automatic directory management, robust error handling, and graceful application shutdown procedures.