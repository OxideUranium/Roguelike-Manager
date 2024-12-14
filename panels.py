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


class Node:
    def __init__(self, name, file_path=""):
        self.name = name
        self.save_file_path = file_path

        # connections in and between timelines
        self.prev_node = None
        self.next_node = None
        self.left_node = None
        self.right_node = None

    def connect(self, direction, node ):
        # connect this node to another node in a certain direction
        if direction == "prev":
            self.next_node = node
            if node.prev_node:
                temp = node.prev_node
                node.prev_node = self
                self.prev_node = temp
        elif direction == "next":
            self.prev_node = node
            if node.next_node:
                temp = node.next_node
                node.next_node = self
                self.next_node = temp
        elif direction == "left":
            self.right_node = node
            if node.left_node:
                temp = node.left_node
                node.left_node = self
                self.left_node = temp
        elif direction == "right":
            self.left_node = node
            if node.right_node:
                temp = node.right_node
                node.right_node = self
                self.right_node = temp

    def disconnect(self, direction):
        # disconnect this node from another node in a certain direction
        if direction == "prev":
            self.prev_node.next_node = None
            self.prev_node = None
        elif direction == "next":
            self.next_node.prev_node = None
            self.next_node = None
        elif direction == "left":
            self.left_node.right_node = None
            self.left_node = None
        elif direction == "right":
            self.right_node.left_node = None
            self.right_node = None
    
    def __repr__(self):
        return f"Node {self.name}, file: {self.save_file_name}"




# a single timeline, a list of nodes
class Timeline:
    def __init__(self, name, first_node=None):
        self.name = name
        self.nodes = []

        if first_node:
            self.nodes.append(first_node)
    
    
    def add_node(self, new_node: Node, selected_node: Node, direction): 
        # a new node can be added from the prev/next/left/right side of the selected node
        # if the direction is left/right, a new timeline is created(since it's a branching event and
        # it's impossible to connect to an existing timeline)

        
        if selected_node not in self.nodes:
            QMessageBox.warning(self, "Warning", "An error occurred: Selected node not found.")
            return

        if direction == "prev":
            selected_node.connect("prev", new_node)
        elif direction == "next":
            selected_node.connect("next", new_node) 
        elif direction == "left":
            selected_node.connect("left", new_node)
        elif direction == "right":
            selected_node.connect("right", new_node)
       





class FolderEventHandler(FileSystemEventHandler):
    def __init__(self, update_callback):
        super().__init__()
        self.update_callback = update_callback

    def on_any_event(self, event):
        # update callback on any events
        self.update_callback()


