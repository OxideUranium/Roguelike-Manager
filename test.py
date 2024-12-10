import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QTextEdit, QListWidget, QGraphicsView, QGraphicsScene, 
    QAction, QMenuBar, QStatusBar
)
from PyQt5.QtCore import Qt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FolderEventHandler(FileSystemEventHandler):
    def __init__(self, update_callback):
        super().__init__()
        self.update_callback = update_callback

    def on_any_event(self, event):
        # update callback on any events
        self.update_callback()

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
        self.observers = Observer()

        self.init_ui()



    def init_ui(self):

        # main widget
        main_widget = QWidget()
        self.main_layout = QVBoxLayout(main_widget)

        # ==TOP menu part
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.file_menu = self.menu_bar.addMenu("File")
        self.edit_menu = self.menu_bar.addMenu("Edit")

        file_menu_open_action = QAction("Open", self)
        file_menu_open_action.triggered.connect(self.select_folder)
        self.file_menu.addAction(file_menu_open_action)

        # ==Content part
        self.content_layout = QHBoxLayout()

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
        self.content_layout.addLayout(left_layout, 2)  
        self.content_layout.addLayout(middle_layout, 2)  
        self.content_layout.addLayout(right_layout, 4) 

        self.main_layout.addLayout(self.content_layout)

        self.setCentralWidget(main_widget)
        

    def init_left_section(self, layout):
        # save file location
        self.left_folder_path_display = QLabel("", self)

        if self.selected_folder == "":
            self.left_folder_path_display.setText("No Folder Selected")
            layout.addWidget(self.left_folder_path_display)
            return
        else:
            # show content of the folder
            self.left_folder_path_display.setText(self.selected_folder)
            layout.addWidget(self.left_folder_path_display)
            file_list = os.listdir(self.selected_folder)
            for file in file_list:
                label = QLabel(file, self)
                layout.addWidget(label)
                label = QLabel(file, self)
                layout.addWidget(label)



    def init_middle_section(self, layout):

        # show saved games (built-in folder "saves")
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
            self.init_left_section(self.content_layout)

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
    
