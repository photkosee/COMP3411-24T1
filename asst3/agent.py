#!/usr/bin/python3
#  agent.py
#  Nine-Board Tic-Tac-Toe Agent starter code
#  COMP3411/9814 Artificial Intelligence
#  CSE, UNSW
#  Yifan Zhu, Phot Koseekrainiramon

import socket
import sys
import numpy as np
import copy

from math import inf

# a board cell can hold:
#   0 - Empty
#   1 - We played here
#   2 - Opponent played here

# the boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int8")
s = [".","X","O"]
curr = 0 # this is the current board to play in

# print a row
def print_board_row(bd, a, b, c, i, j, k):
    print(" "+s[bd[a][i]]+" "+s[bd[a][j]]+" "+s[bd[a][k]]+" | " \
             +s[bd[b][i]]+" "+s[bd[b][j]]+" "+s[bd[b][k]]+" | " \
             +s[bd[c][i]]+" "+s[bd[c][j]]+" "+s[bd[c][k]])

# Print the entire board
def print_board(board):
    print_board_row(board, 1,2,3,1,2,3)
    print_board_row(board, 1,2,3,4,5,6)
    print_board_row(board, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 4,5,6,1,2,3)
    print_board_row(board, 4,5,6,4,5,6)
    print_board_row(board, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 7,8,9,1,2,3)
    print_board_row(board, 7,8,9,4,5,6)
    print_board_row(board, 7,8,9,7,8,9)
    print()

# def min_function

# def minmax():
#     box = 1
#     max_score = -inf
#     max_move = 0
#     while box <= 9:
#         curr_score = min_function()
#         if curr_score > max_score:
#             max_score = curr_score
#             max_move = box
#     return box
lines = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9],
    [1, 5, 9],
    [3, 5, 7]
]

def success_box(box):
    for line in lines:
        elements = [box[line[0]], box[line[1]], box[line[2]]]
        count_1 = elements.count(1)
        count_2 = elements.count(2)
        if count_1 == 3:
            return 1
        elif count_2 == 3:
            return 2
    return 0

def success_all(boards):
    for r in range(1, 10):
        box = boards[r]
        result = success_box(box)
        if result != 0:
            return result
    return 0

def evaluate_box(box):
    score = 0
    for line in lines:
        elements = [box[line[0]], box[line[1]], box[line[2]]]
        count_1 = elements.count(1)
        count_2 = elements.count(2)
        
        # player 1
        if count_1 == 1 and count_2 == 0:
            score += 1
        elif count_1 == 2 and count_2 == 0:
            score += 10

        # player 2
        if count_1 == 0 and count_2 == 1:
            score -= 1
        elif count_1 == 0 and count_2 == 2:
            score -= 10
    
    return score

def evaluate_all(boards):
    score = 0
    for r in range(1, 10):
        box = boards[r]
        score += evaluate_box(box)
    
    return score

def deepCopy(boards):
    copied = []
    for row in boards:
        copied.append([item for item in row])
    return copied

def alphabeta(player, m, boards, alpha, beta, best_move, curr_box, depth):
    best_eval = -inf
    this_move = 0

    # Win and Lose
    succ_player = success_all(boards)
    if (succ_player == 1 and player == 2) or (succ_player == 2 and player == 1):
        return -10000 + m
    if (succ_player == 1 and player == 1) or (succ_player == 2 and player == 2):
        return 10000 - m

    # Max Depth
    if m >= depth:
        if depth % 2 == 0:
            return evaluate_all(boards)
        else:
            return -evaluate_all(boards)

    for r in [5, 1, 3, 7, 9, 4, 6, 2, 8]:
        if boards[curr_box][r] == 0:
            this_move = r
            # make move
            curr_boards = deepCopy(boards)
            curr_boards[curr_box][this_move] = player

            if player == 1:
                this_eval = -alphabeta(2, m + 1, curr_boards, -beta, -alpha, best_move, r, depth)
            else:
                this_eval = -alphabeta(1, m + 1, curr_boards, -beta, -alpha, best_move, r, depth)

            if this_eval > best_eval:
                best_move[m] = this_move
                best_eval = this_eval
                if best_eval > alpha:
                    alpha = best_eval
                    # cutoff
                    if alpha >= beta:
                        return( alpha )

    if this_move == 0:  # no legal moves
        return( 0 )     # DRAW
    else:
        return( alpha )

turn = 0
# choose a move to play
def play():
    global turn
    turn += 1
    print(turn)
    if turn <= 6:
        depth = 5
    elif turn <= 12:
        depth = 6
    elif turn <= 18:
        depth = 7
    else:
        depth = 8
    
    # Find move position
    best_move = np.zeros(10,dtype=np.int32)
    m = 0
    alphabeta(1, m, boards, -inf, inf, best_move, curr, depth)

    # Move
    n = best_move[0]
    place(curr, n, 1)

    return int(n)

# place a move in the global boards
def place( board, num, player ):
    global curr
    curr = num
    boards[board][num] = player

# read what the server sent us and
# parse only the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    # init tells us that a new game is about to begin.
    # start(x) or start(o) tell us whether we will be playing first (x)
    # or second (o); we might be able to ignore start if we internally
    # use 'X' for *our* moves and 'O' for *opponent* moves.

    # second_move(K,L) means that the (randomly generated)
    # first move was into square L of sub-board K,
    # and we are expected to return the second move.
    if command == "second_move":
        # place the first move (randomly generated for opponent)
        place(int(args[0]), int(args[1]), 2)
        return play()  # choose and return the second move

    # third_move(K,L,M) means that the first and second move were
    # in square L of sub-board K, and square M of sub-board L,
    # and we are expected to return the third move.
    elif command == "third_move":
        # place the first move (randomly generated for us)
        place(int(args[0]), int(args[1]), 1)
        # place the second move (chosen by opponent)
        place(curr, int(args[2]), 2)
        return play() # choose and return the third move

    # nex_move(M) means that the previous move was into
    # square M of the designated sub-board,
    # and we are expected to return the next move.
    elif command == "next_move":
        # place the previous move (chosen by opponent)
        place(curr, int(args[0]), 2)
        return play() # choose and return our next move

    elif command == "win":
        print("Yay!! We win!! :)")
        return -1

    elif command == "loss":
        print("We lost :(")
        return -1

    return 0

import time
# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        print(text)
        print("------")
        time.sleep(1)
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()
