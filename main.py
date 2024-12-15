import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QAction, QMessageBox
)
from PyQt5.QtCore import Qt
import panels

class SaveManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Save Manager Test 01")
        self.setGeometry(100, 100, 800, 600)

        # built-in saves folder
        self.saves_folder = "saves"
        self.selected_folder = ""

        if not os.path.exists("saves"):
            os.makedirs("saves")

        self.init_ui()

    def init_ui(self):

        self.init_menubar()

        # main widget
        main_widget = QWidget()
        self.main_layout = QVBoxLayout(main_widget)

        # L, M, R panels and content_layout
        self.content_layout = QHBoxLayout()
        

        """
        self.right_panel = panels.RightPanel(self)
        """
        self.left_panel = panels.LeftPanel(self)
        self.middle_panel = panels.MiddlePanel(self)
        self.right_panel = panels.RightPanel(self)

        self.content_layout.addWidget(self.left_panel, 2)  
        self.content_layout.addWidget(self.middle_panel, 2)  
        self.content_layout.addWidget(self.right_panel, 4) 

        self.main_layout.addLayout(self.content_layout)

        self.setCentralWidget(main_widget)

    def init_menubar(self):
        menu_bar = self.menuBar()
        self.setMenuBar(menu_bar)
        self.file_menu = menu_bar.addMenu("File")
        self.edit_menu = menu_bar.addMenu("Edit")
        self.view_menu = menu_bar.addMenu("View")
        
        
        file_menu_open_action = QAction("Open", self)
        file_menu_open_action.triggered.connect(self.menu_file_open_select_folder)
        self.file_menu.addAction(file_menu_open_action)

        edit_menu_test = QAction("Test", self)
        edit_menu_test.triggered.connect(self.menu_edit_test_action)
        self.edit_menu.addAction(edit_menu_test)

        view_menu_test = QAction("Test", self)
        view_menu_test.triggered.connect(self.menu_view_test_action)
        self.view_menu.addAction(view_menu_test)
        

    def menu_file_open_select_folder(self):
        # select a folder
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.selected_folder = folder_path
            self.left_panel.update_panel()

    def menu_edit_test_action(self):
        popup_window = QMessageBox()
        popup_window.setWindowTitle("Test Popup")
        popup_window.setText("Test popup for Edit menu")
        popup_window.exec_()

    def menu_view_test_action(self):
        popup_window = QMessageBox()
        popup_window.setWindowTitle("Test Popup")
        popup_window.setText("Test popup for View menu")
        popup_window.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SaveManagerApp()
    window.show()
    sys.exit(app.exec_())
    
