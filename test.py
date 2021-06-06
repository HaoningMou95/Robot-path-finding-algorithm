import argparse as ap
import re
import platform
import numpy as np


######## RUNNING THE CODE ####################################################

#   You can run this code from terminal by executing the following command

#   python planpath.py <INPUT/input#.txt> <OUTPUT/output#.txt> <flag>

#   for example: python planpath.py INPUT/input2.txt OUTPUT/output2.txt 0

#   NOTE: THIS IS JUST ONE EXAMPLE INPUT DATA

###############################################################################


################## YOUR CODE GOES HERE ########################################

def graphsearch(map):
    #solution = "S-R-RD-D-D-LD-G"


    start_index = np.argwhere(map == 'S')[0].tolist()
    start_y = start_index[0]
    start_x = start_index[1]
    goal_index = np.argwhere(map == 'G')[0].tolist()
    goal_y = goal_index[0]
    goal_x = goal_index[1]
    map_degree = map.shape[0]
    indentifier = 0
    h = round((((start_index[0]- goal_index[0])** 2 + (start_index[1] - goal_index[1]) ** 2) ** 0.5), 2)
    start_node = {'N'+str(indentifier):['S', [start_x, start_y],0,h,h]}
    openList = start_node
    closelist = {}
    existedNode = [[start_x, start_y]]
    j = 0
    step = 0

    while j == 0:
        if len(openList) > 0:
            minlist = [(i, openList[i][4]) for i in openList]
            current_Ide = min(minlist, key=lambda n:(n[1]))[0]
            current_node={current_Ide:openList[current_Ide]}
            closelist[current_Ide] = openList[current_Ide]
            del openList[current_Ide]
            step+=1
            print()
            print("step" + str(step))
            print()
            y = current_node[current_Ide][1][1]
            x = current_node[current_Ide][1][0]
            existedNode.append([x,y])
            if x != goal_x or y != goal_y:
                movement = {'RD': [x+1,y+1], 'R':[x+1,y], 'RU':[x+1, y-1], 'U':[x, y-1], 'LU':[x-1,y-1], 'L':[x-1,y], 'LD':[x-1,y+1], 'D':[x,y+1]}
                invalid = []
                mountains = {}
                child = {}
                for move in movement:
                    if movement[move][0] < 0 or movement[move][1] < 0 or movement[move][0] >= map_degree or movement[move][1] >= map_degree:
                        invalid.append(move)
                for i in invalid:
                    del movement[i]
                for move in movement: #DELETE the mountain related move
                    if map[movement[move][1], movement[move][0]] == "X":
                        mountains[move] = [movement[move][0], movement[move][1]]

                for move in mountains:
                    if mountains[move][0] == x:
                        movement = {key:val for key, val in movement.items() if val[1] != movement[move][1] }
                    elif mountains[move][1] == y:
                        movement = {key:val for key, val in movement.items() if val[0] != movement[move][0]}
                    else:
                        try:
                            del movement[move]
                        except: BaseException
                for move in movement:
                    if movement[move] not in existedNode:
                        if len(move) == 2:
                            child_g = current_node[current_Ide][2]+1
                        elif len(move) == 1:
                            child_g = current_node[current_Ide][2] + 2
                        child_h = round((((movement[move][1]-goal_y)**2+(movement[move][0]-goal_x)**2)**0.5),2)
                        indentifier+=1
                        current_move = current_node[current_Ide][0]
                        child['N'+str(indentifier )] = [current_move+ '-' +move, movement[move],child_g,child_h,child_g+child_h]



                openList.update(child)
                print('openList')
                print(openList)
                print('closedList')
                print(closelist)
            else:
                print('goal')
                current_node[current_Ide][0] = current_node[current_Ide][0] + "-G"
                print(current_node)
                j = 1
        else:
            print("No path!")
            j = 1







def read_from_file(file_name):
    # You can change the file reading function to suit the way

    # you want to parse the file

    file_handle = open(file_name)
    map = file_handle.readlines()
    degree = int(map[0].strip())
    usedMap = []
    for line in map[1:]:
        line = list(line.strip())
        line = np.array(line)
        usedMap.append(line)
    usedMap = np.array(usedMap)

    return usedMap

map = read_from_file('/Users/barry/Desktop/5047Sample/ass/input2.txt')
graphsearch(map)


