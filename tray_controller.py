from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction,QIcon
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class TrayController:
    def __init__(self,gui_factory,exit_callback):
        
        self.gui_factory = gui_factory
        self.exit_callback = exit_callback
        
        self.viewer = None
        
        self.tray = QSystemTrayIcon()

        self.tray.setIcon(self.get_app_icon())

        self.create_menu()

        self.tray.activated.connect(
            self.tray_clicked
        )

        self.tray.show()

    def create_menu(self):
            
        menu = QMenu()

        self.toggle_action = QAction(
            "Show Window"
        )

        self.exit_action = QAction(
                "Exit"
        )

        self.toggle_action.triggered.connect(
            self.toggle_window
        )

        self.exit_action.triggered.connect(
            self.exit_callback
        )

        menu.addAction(self.toggle_action)
        menu.addSeparator()
        menu.addAction(self.exit_action)

        self.tray.setContextMenu(menu)


    def get_app_icon(self):
        
        icon_path = resource_path("assets/app_icon.ico")

        icon = QIcon(icon_path)
        
        
        if not icon.isNull():
            return icon
        

        return QApplication.style().standardIcon(
            QApplication.style().StandardPixmap.SP_ComputerIcon
        )           
    
    def toggle_window(self):
        if self.viewer is None:
            self.viewer = self.gui_factory()

        if self.viewer.isVisible():
            self.viewer.hide()
            self.toggle_action.setText("Show Window")

        else:
            self.viewer.show()
            self.viewer.raise_()
            self.viewer.activateWindow()
            self.toggle_action.setText("Hide Window")

    def tray_clicked(self,reason):

        if(reason == QSystemTrayIcon.ActivationReason.DoubleClick):
            self.toggle_window()

    def hide(self):
        self.tray.hide()

        if self.viewer:
            self.viewer.close()