from panels import LeftPanel, MiddlePanel, RightPanel, Timeline, Node


node00 = Node("node00", "file00")
node01 = Node("node01", "file01")
node02 = Node("node02", "file02")
node03 = Node("node03", "file03")
node02_1 = Node("node02_1", "file02_1")

timeline00 = Timeline("timeline00", node00)

timeline00.add_node(node01, node00, "next")
timeline00.add_node(node02, node01, "next")


timeline01 = timeline00.branch(node02_1, node02, "right")
timeline00.show_nodes()
print("=============")

timeline01.add_node(node03, node02_1, "next")
timeline01.show_nodes()