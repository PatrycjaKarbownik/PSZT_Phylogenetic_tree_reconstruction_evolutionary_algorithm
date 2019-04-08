"""Simple interface for watching created trees. It is not my proudest piece of code, but it works."""

from tkinter import *
from nodes import *
from collections import deque


class MappedPoint:

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y


# Function that draws lines connecting points a and b. It is also returning new point - center of connection.
def _connect_points(a, b, canvas):
    if b.pos_x > a.pos_x:
        a, b = b, a
    canvas.create_line(a.pos_x, a.pos_y, b.pos_x - 20, a.pos_y)
    canvas.create_line(b.pos_x, b.pos_y, b.pos_x - 20, b.pos_y)
    canvas.create_line(b.pos_x - 20, a.pos_y, b.pos_x - 20, b.pos_y)
    return MappedPoint(b.pos_x - 20, (a.pos_y + b.pos_y) / 2)


# nodes_list is list of nodes in order of connecting them
# seq_list is a list of sequences, which is needed to write them also in right order
def _map_tree(node, nodes_list, seq_list):
    nodes_list.appendleft(node)

    if isinstance(node.left, Leaf):
        seq_list.append(node.left)
    else:
        _map_tree(node.left, nodes_list, seq_list)

    if isinstance(node.right, Leaf):
        seq_list.append(node.right)
    else:
        _map_tree(node.right, nodes_list, seq_list)


def _draw_tree(tree, canvas):
    x = 600
    y = 500
    nodes_list = deque()
    seq_list = list()
    _map_tree(tree, nodes_list, seq_list)

    # points is a dictionary storing points by a nodes and leafs unique numbers
    points = dict()
    for i, seq in enumerate(seq_list, 0):
        canvas.create_text(x, y - i * 20, text=str(seq))
        points[seq.number] = MappedPoint(x - 30, y - i * 20)

    while nodes_list:
        node = nodes_list.popleft()
        point_a = points[node.left.number]
        point_b = points[node.right.number]
        new_point = _connect_points(point_a, point_b, canvas)
        points[node.number] = new_point


def run_graphics(tree):

    def scroll_start(event):
        canvas.scan_mark(event.x, event.y)

    def scroll_move(event):
        canvas.scan_dragto(event.x, event.y, gain=1)

    root = Tk()
    root.title("Phylogenetic tree")
    root.geometry('800x600')

    # These are mainly configurations for scrolling since our trees can get big really fast
    canvas = Canvas(root, width=800, height=600)
    xsb = Scrollbar(root, orient="horizontal", command=canvas.xview)
    ysb = Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(bg="white", yscrollcommand=ysb.set, xscrollcommand=xsb.set)
    canvas.configure(scrollregion=(-1000, -1000, 1000, 1000))

    xsb.grid(row=1, column=0, sticky="ew")
    ysb.grid(row=0, column=1, sticky="ns")
    canvas.grid(row=0, column=0, sticky="nsew")

    canvas.bind("<ButtonPress-1>", scroll_start)
    canvas.bind("<B1-Motion>", scroll_move)

    _draw_tree(tree, canvas)

    root.mainloop()
