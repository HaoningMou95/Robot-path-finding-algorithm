import numpy

class Node:
    def __init__(self, x, y, parent=None):
        self.parent = parent
        self.x = x
        self.y = y

        self.g = 0
        self.h = 0
        self.f = 0

        self.route = ''
        self.id = ''

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y




def readMap(path):

    file = [ch for ch in open(path).read() if ch != '\n' if ch != ' ']
    sizeTemp = file.pop(0)
    # sizeTemp += file.pop(0)

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


class A_star:
    def __init__(self):
        self.opened = []
        self.closed = []
        self.path = []

    def getMinNode(self):
        '''
        get the min cost from the opened list
        :return: the min cost node
        '''
        if len(self.opened) > 0:
            nodeTemp = self.opened[0]
            for node in self.opened:
                if node.g + node.h < nodeTemp.g + nodeTemp.h:
                    nodeTemp = node
            return nodeTemp

    def isInOpenList(self, other):
        for exist_node in self.opened:
            if other == exist_node:
                return True
        return False

    def isInCloseList(self, other):
        for exist_node in self.closed:
            if other == exist_node:
                return True
        return False

    def a_star(self, path):
        map, start, end, size = readMap(path)
        print(map)
        id = 0
        expand_order = 0

        start_node = Node(start[0], start[1], None)
        start_node.h = start_node.g = start_node.f = 0

        goal_node = Node(end[0], end[1], None)
        goal_node.h = goal_node.g = goal_node.f = 0

        direction = {(-1, -1):"LU", (-1, 0):"U", (-1, 1):"RU",
                     ( 0, -1):"L",               ( 0, 1):"R",
                     ( 1, -1):"LD", (1,0):"D",   ( 1, 1):"RD", }

        start_node.id = 'N0'
        start_node.route = 'S'
        self.opened.append(start_node)

        while len(self.opened) > 0:

            current_node = self.getMinNode()
            del self.opened[self.opened.index(current_node)]

            # self.opened.remove(current_node)

            self.closed.append(current_node)

            # print('before if',current_node.x, current_node.y)
            if current_node == goal_node:
                # print(current_node)
                current = current_node
                end_path = current_node.route
                while current is not None:
                    self.path.append([current.x, current.y])
                    current = current.parent

                return self.path[::-1],  end_path+'-G'
                # return self.path, self.opened, self.closed

            children = []

            for dir in direction.keys():
                node_position = [current_node.x + dir[0], current_node.y + dir[1]]

                if node_position[0] > (size - 1) or node_position[0] < 0 \
                   or node_position[1] > (size - 1) or node_position[1] < 0:
                    continue

                if map[node_position[0], node_position[1]] == "X" or map[[current_node.x],[node_position[1]]] == 'X' \
                        or map[[node_position[0]],[current_node.y]] == 'X':
                    continue


                new_node = Node(node_position[0], node_position[1], current_node)
                new_node.route = new_node.parent.route + '-' + direction[dir]
                # if new_node.id == '':
                #     id += 1
                #     new_node.id = 'N' + str(id)
                # if new_node.x == 2 and new_node.y == 0:
                #     print('!!!',new_node.x, new_node.y)
                if not self.isInOpenList(new_node):
                    children.append(new_node)

            for child in children:


                flg = True
                for closed_child in self.closed:

                    if child == closed_child:

                        child.x, child.y = -1, -1
                        flg = False
                        break
                if flg:
                    if (abs(child.x - current_node.x) + abs(child.y - current_node.y)) > 1:
                        child.g = current_node.g + 1
                    else:
                        child.g = current_node.g + 2

                    if child.id == '':
                        id += 1
                        child.id = 'N' + str(id)
                    # child.h = abs(child.x - goal_node.x) if abs(child.x - goal_node.x) > abs(child.y - goal_node.y) else abs(child.y - goal_node.y) #25 24 cost
                    child.h = round((((child.x - goal_node.x) ** 2 + (child.y - goal_node.y) ** 2) / 2 ** 0.5), 2)
                    child.f = round((child.g + child.h), 2)
                    self.opened.append(child)

            expand_order += 1
            print('current node')
            print(current_node.id+': '+str(expand_order),current_node.route, str(current_node.g)+' '
                  +str(current_node.h)+' '+str(current_node.f))
            print('\nchildren')
            for node in children:
                if node.x == -1 and node.y == -1:
                    continue
                print(node.id+':', node.route,' ', end='')
            print('\n\nopen list')
            for node in self.opened:
                print(node.id+':', node.route, str(node.g)+' '+str(node.h)+' '+str(node.f))
            print('\n\nclose list')
            for node in self.closed:
                print(node.id+':', node.route, str(node.g) + ' ' + str(node.h) + ' ' + str(node.f))
            print()
        if len(self.opened) == 0:
            return 'No path', 'No path'



a = A_star()
route, endPath = a.a_star('/Users/mouhaoning/Desktop/input1.txt')
# route = temp[::1]
print(route,endPath)


