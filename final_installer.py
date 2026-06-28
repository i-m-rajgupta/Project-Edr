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

INSTALL_DIR = PROGRAM_FILES / APP_NAME

GUI_PATH = INSTALL_DIR / GUI_NAME
SERVICE_PATH = INSTALL_DIR / SERVICE_NAME

# =========================
# LOGGING
# =========================

LOG_DIR = PROGRAM_DATA / APP_NAME / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "installer.log"

logger = logging.getLogger("EdrInstaller")
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

logger.info("========== INSTALLER STARTED ==========")

def log_step(msg):
    logger.info(msg)

def log_error(msg):
    logger.error(msg)

# =========================
# SERVICE CONTROL
# =========================

def stop_service():
    log_step("Stopping service...")
    subprocess.run(["sc.exe", "stop", SERVICE_INTERNAL_NAME], capture_output=True)

def wait_for_service_stop(name, timeout=20):
    log_step("Waiting for service to fully stop...")

    for _ in range(timeout):
        result = subprocess.run(
            ["sc.exe", "query", name],
            capture_output=True,
            text=True
        )

        if "STOPPED" in result.stdout:
            log_step("Service fully stopped")
            return

        time.sleep(1)

    log_error("Service did not stop in time")

def delete_service():
    log_step("Deleting service from SCM...")
    subprocess.run(["sc.exe", "delete", SERVICE_INTERNAL_NAME], capture_output=True)

def kill_process():
    log_step("Force killing running processes...")

    subprocess.run(["taskkill", "/F", "/IM", GUI_NAME], capture_output=True)
    subprocess.run(["taskkill", "/F", "/IM", SERVICE_NAME], capture_output=True)

# =========================
# REGISTRY CLEANUP
# =========================

def remove_registry():
    log_step("Removing HKLM startup entry...")

    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        ) as key:
            winreg.DeleteValue(key, "EdrAgentGUI")

        log_step("Registry entry removed")

    except FileNotFoundError:
        log_step("Registry entry not found (skipped)")

    except Exception as e:
        log_error(f"Registry cleanup failed: {e}")

# =========================
# FILE CLEANUP (SAFE)
# =========================

def safe_delete(path, retries=5, delay=1):
    for _ in range(retries):
        try:
            if path.exists():
                path.unlink()
                return True
        except PermissionError:
            time.sleep(delay)
    return False

def remove_files():
    log_step("Removing installed files...")

    try:
        if not safe_delete(GUI_PATH):
            log_error("Failed to delete GUI EXE")

        if not safe_delete(SERVICE_PATH):
            log_error("Failed to delete SERVICE EXE")

        try:
            INSTALL_DIR.rmdir()
        except:
            pass

    except Exception as e:
        log_error(f"File cleanup failed: {e}")

# =========================
# INSTALL
# =========================

def install():
    log_step("Starting fresh installation...")

    base_dir = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent

    source_gui = base_dir / GUI_NAME
    source_service = base_dir / SERVICE_NAME

    INSTALL_DIR.mkdir(parents=True, exist_ok=True)

    if not source_gui.exists():
        raise FileNotFoundError("GUI EXE missing")

    if not source_service.exists():
        raise FileNotFoundError("Service EXE missing")

    log_step("Copying files...")

    shutil.copy2(source_gui, GUI_PATH)
    shutil.copy2(source_service, SERVICE_PATH)

    log_step("Files copied successfully")

    # Registry startup
    log_step("Creating startup registry entry...")

    with winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE
    ) as key:

        winreg.SetValueEx(
            key,
            "EdrAgentGUI",
            0,
            winreg.REG_SZ,
            f'"{GUI_PATH}"'
        )

    log_step("Registry startup added")

    # Service install
    log_step("Installing service...")
    subprocess.check_call([str(SERVICE_PATH), "install"])
    log_step("Service installed")

    # Set auto start
    log_step("Setting service startup type to AUTO...")
    subprocess.check_call([
        "sc.exe",
        "config",
        SERVICE_INTERNAL_NAME,
        "start=",
        "auto"
    ])

    log_step("Service set to automatic start")

    # Start service
    subprocess.check_call([str(SERVICE_PATH), "start"])
    log_step("Service started")

# =========================
# MAIN FLOW
# =========================

try:
    log_step("CLEANUP PHASE STARTED")

    stop_service()
    kill_process()
    wait_for_service_stop(SERVICE_INTERNAL_NAME)
    delete_service()
    remove_registry()
    remove_files()

    log_step("CLEANUP COMPLETED")

    install()

    log_step("INSTALLATION SUCCESSFUL")
    logger.info("========== INSTALLER FINISHED SUCCESS ==========")

except Exception as e:
    logger.exception(f"INSTALLATION FAILED: {e}")
    logger.info("========== INSTALLER FAILED ==========")
    raise