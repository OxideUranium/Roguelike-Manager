import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QTextEdit, QListWidget, QGraphicsView, QGraphicsScene
)
from PyQt5.QtCore import Qt

class SaveManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Save Manager Test 01")
        self.setGeometry(100, 100, 800, 600)

        # built-in saves folder
        self.saves_folder = "saves"
        if not os.path.exists("saves"):
            os.makedirs("saves")

        # main widget
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # LEFT
        left_layout = QVBoxLayout()
        self.init_left_section(left_layout)

        # MIDDLE
        middle_layout = QVBoxLayout()
        self.init_middle_section(middle_layout)

        # RIGHT
        right_layout = QVBoxLayout()
        self.init_right_section(right_layout)

        # update main
        main_layout.addLayout(left_layout, 2)  
        main_layout.addLayout(middle_layout, 2)  
        main_layout.addLayout(right_layout, 4) 

        self.setCentralWidget(main_widget)

    def init_left_section(self, layout):
        # save file location
        label = QLabel("Select Save Location:", self)
        label.setAlignment(Qt.AlignLeft)
        layout.addWidget(label)

        # folder selection
        btn_select_folder = QPushButton("Open Folder", self)
        btn_select_folder.clicked.connect(self.select_folder)
        layout.addWidget(btn_select_folder)

        # show path
        self.folder_path_display = QTextEdit(self)
        self.folder_path_display.setReadOnly(True)
        layout.addWidget(self.folder_path_display)


    def init_middle_section(self, layout):

        # show saved games (built-in)
        label = QLabel("Saved Games", self)
        label.setAlignment(Qt.AlignLeft)
        layout.addWidget(label)

        # show
        self.saved_games_list = QListWidget(self)
        self.update_saves_list()
        layout.addWidget(self.saved_games_list)


    def init_right_section(self, layout):

        # canvas, for managing save files
        canvas_label = QLabel("UI (Canvas)", self)
        canvas_label.setAlignment(Qt.AlignCenter)

        # canvas
        scene = QGraphicsScene(self)
        canvas = QGraphicsView(scene, self)
        layout.addWidget(canvas_label)
        layout.addWidget(canvas)

    def select_folder(self):

        # select a folder
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folder_path_display.setText(folder_path)

    def update_saves_list(self):

        # update files
        self.saved_games_list.clear()
        if os.path.exists(self.saves_folder):
            files = os.listdir(self.saves_folder)
            for file in files:
                self.saved_games_list.addItem(file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SaveManagerApp()
    window.show()
    sys.exit(app.exec_())
