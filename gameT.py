import copy

import numpy as np
import pygame
import math
import sys
import random

rows_num = 2
cols_num = 2

agent_num = 1
player_num = 2

board = np.zeros((rows_num, cols_num))
best_path =[]

class Node:

    def __init__(self,board,score):
        self.children =[]
        self.board=board
        self.score=score
    def add_child(self, child):
        self.children.append(child)


def score_h(board):


    return 1



def get_next_valid_slot(board, col):
    for i in reversed(( range(rows_num))):
        if board[i][col] == 0:
            return i


def get_children_board(board, maximizing_player):
    children =[]
    for col in range(cols_num):
        if board[0][col] == 0:
            child_board = copy.deepcopy(board)
            row = get_next_valid_slot(board, col)
            if maximizing_player :
                child_board[row][col] = agent_num
            else :
                child_board[row][col] = player_num

            children.append(child_board)
    return children




def is_terminal(board):

    x = np.count_nonzero(board == 0)
    return x == 0

root =Node(board,score_h(board))



def get_root_children():
    children = get_children_board(board, True)
    for child_board in children:
        child_node = Node(child_board,score_h(child_board))
        root.add_child(child_node)



def min_max(node, depth, maximizing_player):

    board=node.board

    if is_terminal(board) or depth == 0:
        return score_h(board)

    if maximizing_player:
        v = -math.inf
        children = get_children_board(board,True)
        for child_board in children:
            child_node =Node(child_board,score_h(child_board))
            node.add_child(child_node)
            v = max(v, min_max(child_node, depth - 1, False))
        return v
    else:
        v = math.inf
        children = get_children_board(board,False)
        for child_board in children:
            child_node =Node(child_board,score_h(child_board))
            node.add_child(child_node)

            v = min(v, min_max(child_node, depth - 1, True))
        return v



def best_path(root,final_score):
    path =[]
    path.append(root.board)
    current = root
    while not (is_terminal(current.board)):
        for child in current.children :
            if child.score == final_score :
                path.append(child.board)
                current = child
                break

    return path



get_root_children()
final_score = min_max(root,7,True)
root.children.pop(0)
root.children.pop(0)

print(final_score)
print(root.children[1].children[0].children[0].children[0].board)

print(best_path(root,final_score))
