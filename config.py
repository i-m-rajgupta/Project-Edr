from pathlib import Path
import os

APP_DIR = Path(os.getenv("PROGRAMDATA")) / "EdrAgent"

LOG_DIR = APP_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "data.log"