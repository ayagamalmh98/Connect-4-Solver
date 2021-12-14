import copy

import numpy as np
import pygame
import math
import sys
import random

rows_num = 6
cols_num = 7

agent_num = 2
player_num = 1

connect4 = 4

board = np.zeros((rows_num, cols_num))
flatten_board = board.flatten()
str_board = "".join(str(i) for i in flatten_board)
set = {str_board: 1}


#class Node:

#    def __init__(self, board, score):
#        self.children = []
#        self.board = board
#        self.score = score

#    def add_child(self, child):
#        self.children.append(child)
#    def set_board(self, board):
#        self.board = board


def calc_h(connect):
    h = 0
    if connect.count(agent_num) == 2 and connect.count(0) == 2:
        h += 2
    if connect.count(agent_num) == 3 and connect.count(0) == 1:
        h += 5
    elif connect.count(agent_num) == 4:
        h += 20

    if connect.count(player_num) == 3 and connect.count(0) == 1:
        h -= 25
    elif connect.count(player_num) == 2 and connect.count(0) == 2:
        h -= 3


    return h


def score_h(board):
    h = 0
    ## Score center
    center_arr = [int(i) for i in list(board[:, cols_num // 2])]
    center_count = center_arr.count(agent_num)
    h += center_count * 4

    ## Score Horizontal
    for r in range(rows_num):
        row_arr = [int(i) for i in list(board[r, :])]
        for c in range(cols_num - 3):
            connect = row_arr[c:c + connect4]
            h += calc_h(connect)
    ## Score Vertical
    for c in range(cols_num):
        col_arr = [int(i) for i in list(board[:, c])]
        for r in range(rows_num - 3):
            connect = col_arr[r:r + connect4]
            h += calc_h(connect)
    ## Score diagonal
    for r in range(rows_num - 3):
        for c in range(cols_num - 3):
            connect = [board[r + i][c + i] for i in range(connect4)]
            h += calc_h(connect)

    for r in range(rows_num - 3):
        for c in range(cols_num - 3):
            connect = [board[r + 3 - i][c + i] for i in range(connect4)]
            h += calc_h(connect)
    return h


def get_next_valid_slot(board, col):
    for i in reversed((range(rows_num))):
        if board[i][col] == 0:
            return i


# def get_children(board, maximizing_player):
#    # board = node.current_board
#     children = []
#     for col in range(cols_num):
#         if board[0][col] == 0:
#             child_board = copy.deepcopy(board)
#             row = get_next_valid_slot(board, col)
#             if maximizing_player:
#                 child_board[row][col] = agent_num
#             else:
#                 child_board[row][col] = player_num

#             #child_node = Node(child_board, score_h(child_board))
#             children.append(child_board)
#     return children


def is_terminal(board):
    x = np.count_nonzero(board == 0)
    return x == 0


def get_childern(board):
    Childern_cols = []
    for col in range(cols_num):
        if board[0][col] == 0:
            Childern_cols.append(col)
    return Childern_cols

def min_max(board, depth, maximizing_player):
    # board = node.current_board
    children = get_childern(board)
    if is_terminal(board) or depth == 0:
        return score_h(board), None
    if maximizing_player:
        v = -math.inf
        choosen_col = random.choice(children)
        for col in children:
            row = get_next_valid_slot(board, col)
            child_board = board.copy()
            child_board[row][col] = agent_num
            flatten_board = child_board.flatten()
            str_board = "".join(str(i) for i in flatten_board)
            if not (str_board in set):
                set[str_board] = 1
                value = min_max(child_board, depth - 1, False)[0]
                if value > v:
                    choosen_col = col
                    v = value
    else:
        v = math.inf
        choosen_col = random.choice(children)
        for col in children:
            row = get_next_valid_slot(board, col)
            child_board = board.copy()
            child_board[row][col] = player_num
            flatten_board = child_board.flatten()
            str_board = "".join(str(i) for i in flatten_board)
            if not (str_board in set):
                set[str_board] = 1
                value = min_max(child_board, depth - 1, True)[0]
                if value < v:
                    choosen_col = col
                    v = value
    return v, choosen_col


# def min_max_ab(board, depth,alpha, beta, maximizing_player):
#     #board = node.current_board

#     if is_terminal(board) or depth == 0:
#         return score_h(board), None
#     if maximizing_player:
#         v = -math.inf
#         children = get_children(board, True)
#         choosen_child = children[0]
#         for child in children:
#             #node.add_child(child)

#             value= min_max(child, depth - 1, False)[0]
#             if value > v :
#                 choosen_child = child
#                 v = value
#             #node.score = v
#             alpha = max(alpha, v)
#             if alpha >= beta:
#                 break
#         return v,choosen_child
#     else:
#         v = math.inf
#         children = get_children(board, False)
#         choosen_child = children[0]
#         for child in children:
#             #node.add_child(child)
#             value = min_max(child, depth - 1, True)[0]
#             if value < v :
#                 choosen_child = child
#                 v = value
#             beta = min(beta, v)
#             if alpha >= beta:
#                 break
#             #node.score = v
#         return v,choosen_child

# def min_max(board, depth, maximizing_player):
#     # board = node.current_board

#     if is_terminal(board) or depth == 0:
#         return score_h(board), None
#     if maximizing_player:
#         v = -math.inf
#         children = get_children(board, True)
#         choosen_child = children[0]
#         for child in children:
#             # node.add_child(child)
#             flatten_board = child.flatten()
#             str_board = "".join(str(i) for i in flatten_board)
#             if not (str_board in set):
#                 set[str_board] = 1
#                 value = min_max(child, depth - 1, False)[0]
#                 if value > v:
#                     choosen_child = child
#                     v = value
#                 # no = {}de.score = v
#         return v, choosen_child
#     else:
#         v = math.inf
#         children = get_children(board, False)
#         choosen_child = children[0]
#         for child in children:
#             flatten_board = child.flatten()
#             str_board = "".join(str(i) for i in flatten_board)
#             if not (str_board in set):
#                 set[str_board] = 1
#                 # node.add_child(child)
#                 value = min_max(child, depth - 1, True)[0]
#                 if value < v:
#                     choosen_child = child
#                     v = value
#             # node.score = v
#         return v, choosen_child


def best_path(node, final_score):
    path = []
    path.append(node.board)
    current = node
    depth = 4
    print("hereu")

    while (not (is_terminal(current.board))) and depth > 0:
        for child in current.children:
            if child.score == final_score:
                path.append(child.board)
                current = child
                break
    print("hered")

    return path