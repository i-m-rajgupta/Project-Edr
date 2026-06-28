from pathlib import Path
import os

APP_DIR = Path(os.getenv("PROGRAMDATA")) / "EdrAgent"


LOG_FILE = APP_DIR / "data.log"