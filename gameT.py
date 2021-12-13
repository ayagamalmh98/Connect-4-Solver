







import copy

import numpy as np
import pygame
import math
import sys
import random

rows_num = 6
cols_num = 7

agent_num = 1
player_num = 2

connect4 = 4

board = np.zeros((rows_num, cols_num))


class Node:

    def __init__(self,board,score):
        self.children =[]
        self.board=board
        self.score=score

    def add_child(self, child):
        self.children.append(child)


def calc_h(connect):
    h = 0
    player = agent_num
    opponent = player_num

    if connect.count(player) == 2 and connect.count(0) == 2:
        h += 2
    elif connect.count(player) == 3 and connect.count(0) == 1:
        h += 5
    elif connect.count(player) == 4:
        h += 1000
        
    if connect.count(opponent) == 2 and connect.count(0) == 2:
        h -= 2
    elif connect.count(opponent) == 3 and connect.count(0) == 1:
        h -= 100

    return h

def score_h(board):
    h = 0
    ## Score Horizontal
    for r in range(rows_num):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(cols_num-3):
            connect = row_array[c:c+connect4]
            h += calc_h(connect)
    ## Score Vertical
    for c in range(cols_num):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(rows_num-3):
            connect = col_array[r:r+connect4]
            h += calc_h(connect)
    ## Score diagonal
    for r in range(rows_num-3):
        for c in range(cols_num-3):
            connect = [board[r+i][c+i] for i in range(connect4)]
            h += calc_h(connect)

    for r in range(rows_num-3):
        for c in range(cols_num-3):
            connect = [board[r+3-i][c+i] for i in range(connect4)]
            h += calc_h(connect)
    return h


def get_next_valid_slot(board, col):
    for i in reversed(( range(rows_num))):
        if board[i][col] == 0:
            return i


def get_children(node, maximizing_player):
    board=node.board
    children =[]
    for col in range(cols_num):
        if board[0][col] == 0:
            child_board = copy.deepcopy(board)
            row = get_next_valid_slot(board, col)
            if maximizing_player :
                child_board[row][col] = agent_num
            else :
                child_board[row][col] = player_num

            child_node =Node(child_board,score_h(child_board))
            children.append(child_node)
    return children




def is_terminal(board):

    x = np.count_nonzero(board == 0)
    return x == 0

root =Node(board,score_h(board))



def get_root_children():
    children = get_children(root, True)
    for child in children:
        root.add_child(child)



def min_max(node, depth, maximizing_player):

    board=node.board

    if is_terminal(board) or depth == 0:
        return score_h(board)

    if maximizing_player:
        v = -math.inf
        children = get_children(node,True)
        for child in children:
            node.add_child(child)
            v = max(v, min_max(child, depth - 1, False))
            node.score =v
        return v
    else:
        v = math.inf
        children = get_children(node,False)
        for child in children:
            node.add_child(child)
            v = min(v, min_max(child, depth - 1, True))
            node.score =v
        return v



def best_path(node,final_score):
    path =[]
    path.append(node.board)
    current = node
    depth =7
    while not (is_terminal(current.board)) and depth > 0 :
        for child in current.children :
            if child.score == final_score :
                path.append(child.board)
                current = child
                break

    return path



get_root_children()
final_score = min_max(root,7,True)
new_board = copy.deepcopy(board)
children = get_children(root, True)
for child in children :
    if child.score == final_score :
        new_board = child.board
        break



new_root = Node(new_board,root.score)
# number of branches in 1st level !!
root.children.pop(0)
root.children.pop(0)

print(best_path(root,final_score))
print(new_root.board)

#get player move now
#new_root

while True:
    pass
    #min_max(new_root,7,True)
    #player turn now