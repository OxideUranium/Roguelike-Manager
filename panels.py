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

class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.selected_folder = ""

        self.file_menu = self.addMenu("File")
        self.edit_menu = self.addMenu("Edit")
        self.view_menu = self.addMenu("View")
        self.help_menu = self.addMenu("Help")
        
        file_menu_open_action = QAction("Open", parent)
        file_menu_open_action.triggered.connect(self.select_folder)
        self.file_menu.addAction(file_menu_open_action)

    def select_folder(self):
        # select a folder
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.parent.selected_folder = folder_path


class LeftPanel(QWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.folder_path = ""

        self.layout = QVBoxLayout(self)
        self.folder_label = QLabel("No Folder Selected", self.parent)
        self.layout.addWidget(self.folder_label)

    def update_panel(self, folder_path):
        while self.count():
            item = self.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not folder_path:
            self.folder_label.setText("No Folder Selected")
            self.addWidget(self.folder_label)
        else:
            self.folder_label.setText(f"Folder: {folder_path}")
            self.addWidget(self.folder_label)

            file_list = os.listdir(folder_path)
            for file in file_list:
                file_label = QLabel(file, self.parent)
                self.addWidget(file_label)



class MiddlePanel(QWidget):
    def __init__(self, parent, saves_folder):
        super().__init__(parent)
        self.parent = parent
        self.saves_folder = saves_folder
        self.saved_games_list = QListWidget(self.parent)
        self.layout = QVBoxLayout(self)

        self.init_ui(self.layout)

    def init_ui(self, layout):

        # show saved games (built-in folder "saves")
        label = QLabel("Saved Games")
        label.setAlignment(Qt.AlignLeft)
        layout.addWidget(label)

        # show
        self.saved_games_list = QListWidget(self)
        self.update_saves_list()
        layout.addWidget(self.saved_games_list)

    def update_saves_list(self):

        # update files
        self.saved_games_list.clear()
        if os.path.exists(self.saves_folder):
            files = os.listdir(self.saves_folder)
            for file in files:
                self.saved_games_list.addItem(file)


class RightPanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.init_ui(self.layout)

    def init_ui(self, layout):

        # canvas, for managing save files
        canvas_label = QLabel("UI (Canvas)", self)
        canvas_label.setAlignment(Qt.AlignCenter)

        # canvas
        scene = QGraphicsScene(self)
        canvas = QGraphicsView(scene, self)
        layout.addWidget(canvas_label)
        layout.addWidget(canvas)



class FolderEventHandler(FileSystemEventHandler):
    def __init__(self, update_callback):
        super().__init__()
        self.update_callback = update_callback

    def on_any_event(self, event):
        # update callback on any events
        self.update_callback()


