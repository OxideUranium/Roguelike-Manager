import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QTextEdit, QListWidget, QGraphicsView, QGraphicsScene, 
    QAction, QMenuBar, QStatusBar
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
        if not os.path.exists("saves"):
            os.makedirs("saves")

        self.selected_folder = ""

        self.init_ui()



    def init_ui(self):

        # main widget
        main_widget = QWidget()
        self.main_layout = QVBoxLayout(main_widget)

        # ==TOP menu bar part
        self.menu_bar = panels.MenuBar(self)
        self.setMenuBar(self.menu_bar)

        # L, M, R panels and content_layout
        self.content_layout = QHBoxLayout()
        

        self.left_panel = panels.LeftPanel(self)


        self.middle_panel = panels.MiddlePanel(self, self.saves_folder)
        self.right_panel = panels.RightPanel(self)

        self.content_layout.addWidget(self.left_panel, 2)  
        self.content_layout.addWidget(self.middle_panel, 2)  
        self.content_layout.addWidget(self.right_panel, 4) 

        self.main_layout.addLayout(self.content_layout)

        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SaveManagerApp()
    window.show()
    sys.exit(app.exec_())
    
