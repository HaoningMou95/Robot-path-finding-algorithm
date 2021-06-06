import numpy

def readMap(path):
    file = [ch for ch in open(path).read() if ch != '\n' if ch != ' ']
    sizeTemp = file.pop(0)
    size = int(sizeTemp)
    map = numpy.array(file).reshape(size, size)
    start = [0,0]
    end = [0,0]

    for i in range(size):
        for j in range(size):
            if map[i,j] == 'S':
                start = [i,j]
            if map[i,j] == 'G':
                end = [i,j]

    return map,start,end,size

class Node:
    def __init__(self, x, y, parent=None):
        self.parent = parent
        self.id = 0
        self.x = x
        self.y = y

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def manhattan(self, endNode):
        self.h = (abs(endNode.x - self.x) + abs(endNode.y - self.y))

def astar(path):
    openList = []
    closedList = []
    route = []
    map, start, end, size = readMap(path)

    start_node = Node(start[0], start[1], None)
    start_node.h = start_node.g = start_node.f = 0

    goal_node = Node(end[0], end[1], None)
    goal_node.h = goal_node.g = goal_node.f = 0

    direction = {(-1, 1): "LU", (0, 1): "U", (1, 1): "RU",
                 (-1, 0): "L", (1, 0): "R",
                 (-1, -1): "LD", (0, -1): "D", (1, -1): "RD", }

    openList.append(start_node)
    while openList > 0:
        current_node = openList[0]
        closedList.append(current_node)

        if current_node == goal_node:
            current = current_node
            while current is not None:
                route.append([current.x, current.y])
                current = current.parent
            return route[::1]

        children = []
        for d in direction.keys():
            node_position = [current_node.x + d[0], current_node.y + d[1]]
            if node_position[0] > (size - 1) or node_position[0] < 0 \
                    or node_position[1] > (size - 1) or node_position[1] < 0:
                continue

            if map[node_position[0], [node_position[1]]] != "X":
                continue

            new_node = Node(node_position[0], node_position[1], current_node)
            children.append(new_node)


