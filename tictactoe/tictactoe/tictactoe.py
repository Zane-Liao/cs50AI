"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # X and 0
    if board == terminal(board) and terminal(board) == True:
        return None
    
    if board == initial_state():
        return X
    
    count_X = sum(col == X for row in board for col in row)
    count_O = sum(col == O for row in board for col in row)

    if count_X > count_O:
        return O

    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if board == terminal(board):
        return None
    
    action = set()
    
    # Scanning
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action.add((i, j))

    return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise NameError("action error")

    new_board = copy.deepcopy(board)

    new_player = player(board)

    i, j = action
    new_board[i][j] = new_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win_X = ["X"] * 3
    win_O = ["O"] * 3

    for i in range(3):
        if board[i] == win_X or [b[i] for b in board] == win_X:
            return X
        elif board[i] == win_O or [b[i] for b in board] == win_O:
            return O
    
    if [board[i][i] for i in range(len(board))] == win_X:
        return X
    elif [board[i][i] for i in range(len(board))] == win_O:
        return O
    elif [board[i][len(board) - 1- i] for i in range(len(board))] == win_X:
        return X
    elif [board[i][len(board) - 1- i] for i in range(len(board))] == win_O:
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
            
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # terminal board
    if terminal(board):
        return None
    
    def max_value(board):
        """
        """
        value = float('-inf')
        best_action = None

        if terminal(board):
            return utility(board), None
        
        for action in actions(board):
            min_v, _ = min_value(result(board, action))
            if min_v > value:
                value = min_v
            best_action = action
        
        return value, best_action
    
    def min_value(board):
        """
        """
        value = float('inf')
        best_action = None

        if terminal(board):
            return utility(board), None
        
        for action in actions(board):
            max_v, _ = max_value(result(board, action))
            if max_v < value:
                value = max_v
                best_action = action
        
        return value, best_action

    if player(board) == X:
        _, action = max_value(board)
    
    if player(board) == O:
        _, action =  min_value(board)

    return action