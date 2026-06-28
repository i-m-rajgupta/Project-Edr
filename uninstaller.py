import os
import sys
import shutil
import subprocess
import winreg
import ctypes
import logging
import time
from pathlib import Path

# =========================
# CONFIG
# =========================

APP_NAME = "EdrAgent"
GUI_NAME = "EdrAgentGUI.exe"
SERVICE_NAME = "EdrAgentSERVICE.exe"
SERVICE_INTERNAL_NAME = "EdrHeartbeatAgent"


# =========================
# ADMIN CHECK
# =========================

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    raise PermissionError("Run as Administrator")

# =========================
# PATHS
# =========================

PROGRAM_FILES = Path(os.environ["ProgramFiles"])
PROGRAM_DATA = Path(os.getenv("PROGRAMDATA", "C:\\ProgramData"))
TEMP_DIR = Path(os.getenv("TEMP"))


INSTALL_DIR = PROGRAM_FILES / APP_NAME
PROGRAM_DATA_DIR = PROGRAM_DATA / APP_NAME

GUI_PATH = INSTALL_DIR / GUI_NAME
SERVICE_PATH = INSTALL_DIR / SERVICE_NAME

# =========================
# LOGGING
# =========================

LOGGING_ACTIVE = True

LOG_DIR = PROGRAM_DATA / APP_NAME / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "uninstaller.log"

logger = logging.getLogger("EdrUninstaller")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.handlers.clear()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("========== UNINSTALLER STARTED ==========")

def log_step(msg):
    if LOGGING_ACTIVE:
        logger.info(msg)

def log_error(msg):
    if LOGGING_ACTIVE:
        logger.error(msg)

# =========================
# SERVICE CONTROL
# =========================

def stop_service():
    log_step("Stopping service...")
    subprocess.run(["sc.exe", "stop", SERVICE_INTERNAL_NAME], capture_output=True)

def wait_for_stop(name, timeout=20):
    log_step("Waiting for service to stop...")

    for _ in range(timeout):
        result = subprocess.run(
            ["sc.exe", "query", name],
            capture_output=True,
            text=True
        )

        if "STOPPED" in result.stdout:
            log_step("Service stopped")
            return

        time.sleep(1)

    log_error("Service did not stop in time")

def delete_service():
    log_step("Deleting service...")
    subprocess.run(["sc.exe", "delete", SERVICE_INTERNAL_NAME], capture_output=True)

def kill_processes():
    log_step("Killing running processes...")
    subprocess.run(["taskkill", "/F", "/IM", GUI_NAME], capture_output=True)
    subprocess.run(["taskkill", "/F", "/IM", SERVICE_NAME], capture_output=True)

# =========================
# REGISTRY CLEANUP
# =========================

def remove_registry():
    log_step("Removing startup registry entry...")

    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        ) as key:
            try:
                winreg.DeleteValue(key, "EdrAgentGUI")
                log_step("Registry entry removed")
            except FileNotFoundError:
                log_step("Registry entry not found")

    except Exception as e:
        log_error(f"Registry cleanup failed: {e}")

# =========================
# FILE CLEANUP
# =========================

def safe_delete(path, retries=5, delay=1):
    for _ in range(retries):
        try:
            if path.exists():
                path.unlink()
                return True
        except PermissionError:
            time.sleep(delay)
        except Exception:
            time.sleep(delay)
    return False

def remove_files():
    log_step("Removing installed files...")

    try:
        if not safe_delete(GUI_PATH):
            log_error("Failed to delete GUI EXE")

        if not safe_delete(SERVICE_PATH):
            log_error("Failed to delete SERVICE EXE")

        # remove directory if empty
        try:
            INSTALL_DIR.rmdir()
        except:
            pass

    except Exception as e:
        log_error(f"File cleanup failed: {e}")

def shutdown_logging():
    logger.info("Shutting down logging system...")
    try:
        logging.shutdown()
    except:
        pass

    

    # wait for file handle release
    time.sleep(1)

def remove_program_data():
    log_step("Removing ProgramData folder...")
    global LOGGING_ACTIVE

    try:
        LOGGING_ACTIVE = False
        shutdown_logging()

        if PROGRAM_DATA_DIR.exists():
            shutil.rmtree(PROGRAM_DATA_DIR, ignore_errors=False)
            log_step("ProgramData folder removed")
        else:
            log_step("ProgramData folder not found")
    except Exception as e:
        log_error(f"Failed to remove ProgramData folder: {e}")

def schedule_install_folder_delete():
    folder = str(INSTALL_DIR)

    cmd = (
        f'cmd /c "'
        f'timeout /t 3 >nul & '
        f'cd /d C:\\ & '
        f'rmdir /s /q \"{folder}\"'
        f'"'
    )

    subprocess.Popen(
        cmd,
        shell=True,
        creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
    )



MOVEFILE_DELAY_UNTIL_REBOOT = 0x4

def schedule_self_delete():
    exe_path = sys.executable  # running uninstaller.exe

    ctypes.windll.kernel32.MoveFileExW(
        exe_path,
        None,
        MOVEFILE_DELAY_UNTIL_REBOOT
    )

# =========================
# MAIN FLOW
# =========================

try:
    log_step("UNINSTALL PHASE STARTED")

    stop_service()
    wait_for_stop(SERVICE_INTERNAL_NAME)
    kill_processes()
    delete_service()
    remove_registry()
    remove_files()
    remove_program_data()

    schedule_install_folder_delete()
    schedule_self_delete()


except Exception as e:
    logger.exception(f"UNINSTALLATION FAILED: {e}")
    logger.info("========== UNINSTALLER FAILED ==========")
    raise