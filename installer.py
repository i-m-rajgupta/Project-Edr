import os
import sys
import shutil
import winreg
import logging
from pathlib import Path

APP_NAME = "EdrAgent.exe"

# =========================
# BASE DIRECTORY (CRITICAL FIX)
# =========================
BASE_DIR = Path(sys.executable).parent

# Source (same folder as installer.exe)
source_exe = BASE_DIR / APP_NAME

# Install locations
install_dir = Path(os.environ["ProgramFiles"]) / "EdrAgent"
target_exe = install_dir / APP_NAME

# Logs (ProgramData)
program_data = os.getenv("PROGRAMDATA")
log_dir = Path(program_data) / "EdrAgent" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

log_file = log_dir / "installer.log"

# =========================
# LOGGING SETUP
# =========================
logger = logging.getLogger("EdrInstaller")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log_system_info():
    logger.debug(f"BASE_DIR: {BASE_DIR}")
    logger.debug(f"Source EXE: {source_exe}")
    logger.debug(f"Install Dir: {install_dir}")
    logger.debug(f"Target EXE: {target_exe}")


try:
    logger.info("Installation started")

    log_system_info()

    # Ensure install directory exists
    install_dir.mkdir(parents=True, exist_ok=True)
    logger.debug("Install directory ensured")

    # Validate source file
    if not source_exe.exists():
        logger.error(f"Missing source file: {source_exe}")
        logger.error(f"Files in BASE_DIR: {[p.name for p in BASE_DIR.iterdir()]}")
        raise FileNotFoundError(f"Missing: {source_exe}")

    # Copy EXE
    logger.info("Copying EdrAgent.exe to Program Files...")
    shutil.copy2(source_exe, target_exe)
    logger.info("Copy completed")

    # Verify installation
    if target_exe.exists():
        logger.info(f"Installed at: {target_exe}")
    else:
        logger.error("Installation verification failed")

    # Add startup (ALL USERS)
    logger.info("Adding registry startup entry...")

    with winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE
    ) as key:

        winreg.SetValueEx(
            key,
            "EdrAgent",
            0,
            winreg.REG_SZ,
            str(target_exe)
        )

    logger.info("Startup registry entry added")
    logger.info("Installation completed successfully")

except Exception as e:
    logger.exception(f"Installation failed: {e}")
    raise