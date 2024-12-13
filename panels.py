import os
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QGraphicsView, QGraphicsScene, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LeftPanel(QWidget): 
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.layout = QVBoxLayout(self)
        
        # topic label
        topic_label = QLabel("Game Files", self)
        topic_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(topic_label)

        # display layout
        self.file_list = QListWidget(self)
        self.update_panel()
        self.layout.addWidget(self.file_list)

    def update_panel(self):
        self.file_list.clear()
        if self.parent.selected_folder == "":
            self.file_list.addItem("No folder selected")
        else:
            files = os.listdir(self.parent.selected_folder)
            for file in files:
                self.file_list.addItem(file)


class MiddlePanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # self.parnet.saves_folder
        self.layout = QVBoxLayout(self)

        # topic label
        topic_label = QLabel("Saved Files", self)
        topic_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(topic_label)

        # show saved games (built-in folder "saves")
        self.saved_games_list = QListWidget(self)
        self.update_saves_list()
        self.layout.addWidget(self.saved_games_list)

    def update_saves_list(self):

        # update files
        self.saved_games_list.clear()
        # self.parent.saves_folder must exist
        files = os.listdir(self.parent.saves_folder)
        for file in files:
            self.saved_games_list.addItem(file)

"""
RightPanel structure:
Timelin00 | Timeline01 | Timeline02 | ...
save_01   | X          | X          | ...
save_02   + save_02_1  | X          | ... # user selected a different option in a branching event  
save_03   | save_03    | X          | ...
save_04   | save_04    + save_04_1  | ... # another branching event
...



"""



class RightPanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.layout = QVBoxLayout(self)

        self.timelines = []
        self.create_timeline("Timeline00")

    def show_node_menu(self):
        # after right-clicking on a node
        pass

    def node_selected(self):
        # after clicking on a node
        pass
    
    def create_node(self, node_name):
        # create a new node in the selected timeline
        pass

    def show_timeline_menu(self):
        # after right-clicking on a timeline
        pass

    def create_timeline(self, timeline_name):
        # create a new timeline, a whole new timeline[]
        pass


    



class FolderEventHandler(FileSystemEventHandler):
    def __init__(self, update_callback):
        super().__init__()
        self.update_callback = update_callback

    def on_any_event(self, event):
        # update callback on any events
        self.update_callback()


