import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from log_viewer import LogViewer
from tray_controller import TrayController


from config import LOG_FILE

class AgentController:

    def __init__(self):
        self.app = QApplication(sys.argv)


        self.app.setQuitOnLastWindowClosed(False)

        self.gui_factory = lambda: LogViewer()

        self.tray = TrayController(
            gui_factory=self.gui_factory,
            exit_callback=self.shutdown 
        )
        

    def start(self):
        print("[SYSTEM] Starting Daemon Agent")
        return self.app.exec()
        

    def shutdown(self):
        print("[SYSTEM] Shutting down UI Only..")

        self.tray.hide()
        if self.tray.viewer:
            self.tray.viewer.close()
        self.app.quit()
        

def main():
    controller = AgentController()
    exit_code = controller.start()
    sys.exit(exit_code)
        

if __name__ == "__main__":
    main()



