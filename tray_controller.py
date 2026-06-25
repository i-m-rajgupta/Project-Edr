from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction,QIcon

class TrayController:
    def __init__(self,viewer,exit_callback):
        
        self.viewer = viewer
        self.exit_callback = exit_callback

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
            "Show Window",
            self.tray
        )

        self.exit_action = QAction(
                "Exit",
                self.tray
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
        
        icon_path = "assets/app_icon.png"

        icon = QIcon(icon_path)

        if not icon.isNull():
            print("Icon exited ")
            return icon

        return QApplication.style().standardIcon(
            QApplication.style().StandardPixmap.SP_ComputerIcon
        )           
    
    def toggle_window(self):
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