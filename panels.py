import os
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame,
    QLabel, QListWidget, QGraphicsView, QGraphicsScene, QMessageBox, QSizePolicy, QScrollArea
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
        self.layout = QVBoxLayout(self)

        # topic label
        topic_label = QLabel("Timeline Manager", self)
        topic_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(topic_label)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)


        # 创建滚动区域
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)  # 内容区域大小自适应
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # 创建滚动区域内部的 Widget 和布局
        self.content_widget = QWidget()
        self.content_layout = QHBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignTop)  # 向上对齐
        self.content_layout.setSpacing(20)  # Timeline 之间的间距

        # 将内容布局添加到滚动区域
        self.scroll_area.setWidget(self.content_widget)
        self.main_layout.addWidget(self.scroll_area)

        self.layout.addLayout(self.main_layout)

        self.timelines = []
        self.add_timeline("Timeline00")
        self.add_timeline("Timeline01")

    def add_timeline(self, name):
        # create a new timeline
        # outer frame
        timeline_frame = QFrame(self)
        timeline_frame.setFrameShape(QFrame.StyledPanel)
        timeline_frame.setFixedWidth(150)  # the width of the timeline
        timeline_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # inner layout: vertical
        timeline_layout = QVBoxLayout(timeline_frame)
        timeline_layout.setAlignment(Qt.AlignTop)
        timeline_layout.setSpacing(10)  # the space between nodes

        # topic label
        title_label = QLabel(name, self)
        title_label.setAlignment(Qt.AlignCenter)
        timeline_layout.addWidget(title_label)

        # example nodes
        for i in range(5):
            node_button = QPushButton(f"Node {i + 1}", self)
            node_button.setFixedHeight(50)
            node_button.clicked.connect(lambda _, n=i: self.node_clicked(name, n))
            timeline_layout.addWidget(node_button)

        self.content_layout.addWidget(timeline_frame)

    def node_clicked(self, timeline_name, node_index):
        # test
        QMessageBox.information(self, "Node Clicked", f"Clicked on Node {node_index + 1} in {timeline_name}")

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

    def connect(self, direction:str, node ):
        # connect this node to another node in a certain direction
        #      prev
        #       |
        # left-node-right
        #       |
        #      next

        if direction == "prev":
            self.prev_node = node
            if node.next_node:
                temp = node.next_node
                node.next_node = self
                self.next_node = temp
            else:
                node.next_node = self
        elif direction == "next":
            self.next_node = node
            if node.prev_node:
                temp = node.prev_node
                node.prev_node = self
                self.prev_node = temp
            else:
                node.prev_node = self
        elif direction == "left":
            self.left_node = node
            if node.right_node:
                temp = node.right_node
                node.right_node = self
                self.right_node = temp
            else:
                node.right_node = self
        elif direction == "right":
            self.right_node = node
            if node.left_node:
                temp = node.left_node
                node.left_node = self
                self.left_node = temp
            else:
                node.left_node = self

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
        return f" || Node: {self.name}, file: {self.save_file_path}.|| "
    
    def related_nodes(self):
        # return all the nodes that this node is connected to
        return [self.prev_node, self.next_node, self.left_node, self.right_node]




# a single timeline, contains only one column of nodes
class Timeline:
    def __init__(self, name, first_node=None):
        self.name = name
        self._nodes = []
        self.first_node = first_node

        if first_node:
            self._nodes.append(first_node)
    
    
    def add_node(self, new_node: Node, selected_node: Node, direction): 
        # a new node can be added from the prev/next side of the selected node
        
        if selected_node not in self._nodes:
            QMessageBox.warning(self, "Warning", "An error occurred: Selected node not found.")
            return

        if direction == "prev":
            selected_node.connect("prev", new_node)
            self._nodes.append(new_node)
        elif direction == "next":
            selected_node.connect("next", new_node) 
            self._nodes.append(new_node)
    
    def branch(self, new_node: Node, selected_node: Node, direction: str):
        # if the direction is left/right, a new timeline is created(since it's a branching event and
        # it's impossible to connect to an existing timeline)
        # Therefore, connecting to the left and right will not add to the current timeline
        # but create and return a new timeline

        if selected_node not in self._nodes:
            QMessageBox.warning(self, "Warning", "An error occurred: Selected node not found.")
            return
        
        if direction == "left":
            selected_node.connect("left", new_node)
            new_timeline = Timeline(f"{self.name}_+_{new_node.name}", new_node)
        elif direction == "right":
            selected_node.connect("right", new_node)
            new_timeline = Timeline(f"{self.name}_+_{new_node.name}", new_node)

        return new_timeline

    def show_nodes(self):
        # show the timeline in two method: linked list and list
        print( f"Timeline: {self.name}, node list: {self._nodes}" )
        print("And linked list:")
        current_node = self.first_node
        while current_node:
            print(current_node)
            print(current_node.related_nodes())
            if current_node.next_node:
                print("==V==")
            else:
                print("==X==")
            current_node = current_node.next_node





class FolderEventHandler(FileSystemEventHandler):
    def __init__(self, update_callback):
        super().__init__()
        self.update_callback = update_callback

    def on_any_event(self, event):
        # update callback on any events
        self.update_callback()


