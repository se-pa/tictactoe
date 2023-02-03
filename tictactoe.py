"""
Tic Tac Toe Player made by SP
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count sum of X in board
    count_x = sum([row.count(X) for row in board])
    # Count sum of O in board
    count_o = sum([row.count(O) for row in board])

    # X starts, so if count X > O return O
    if count_x > count_o:
        return O

    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Empty set for actions
    actions = set()

    # for each row in lenght of board
    for row in range(len(board)):
        # for each cell in lenght of row
        for cell in range(len(board[0])):
            # If empty add tuple to set
            if board[row][cell] == EMPTY:
                tuplee = (row, cell)
                actions.add(tuplee)

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # split action into two positions
    i, j = action
    # Deep copy board
    new_board = copy.deepcopy(board)

    # if new action field is not empty raise error
    if new_board[i][j] != EMPTY:
        raise Exception("Action not Valid")

    # return new board with action of current player
    new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # count same signs in row and return if winner
    for row in board:
        if row.count(row[0]) == len(row) and EMPTY not in row:
            return row[0]

    # rorate board and count signs in row and return if winner
    rorate_board = []
    for row in zip(*board):
        rorate_board.append(list(reversed(row)))

    for row in rorate_board:
        if row.count(row[0]) == len(row) and EMPTY not in row:
            return row[0]

    # Check for diagonal and other diagonal, if they are the same return sign
    diagonal = []
    other_diagonal = []
    lenght = len(board)
    for i in range(lenght):
        diagonal.append(board[i][i])
        other_diagonal.append(board[i][lenght - i - 1])

    if all(x == diagonal[0] for x in diagonal):
        return diagonal[0]
    elif all(x == other_diagonal[0] for x in other_diagonal):
        return other_diagonal[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If there is winner return True
    if winner(board) != EMPTY:
        return True

    # Check for empty space in board
    check = True

    for row in board:
        if EMPTY in row:
            check = False

    return check


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Check for max player
    if winner(board) == X:
        return 1
    # Check for min player
    elif winner(board) == O:
        return -1
    # check for tie
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If game is over return None
    if terminal(board):
        return None

    # Create empty lits for optimal actions and list of max or min results
    optimal_actions = []
    results = []

    if player(board) == X:

        # Check every option with for opposite player and append max value to optimal actions
        for action in actions(board):
            option = (min_value(result(board, action)), action)
            optimal_actions.append(option)

        # Check if there are many maximum values for random choice
        for tuple in optimal_actions:
            maximum = max(optimal_actions)
            if tuple[0] == maximum[0]:
                results.append(tuple[1])

    else:

        for action in actions(board):

            option = ((max_value(result(board, action))), action)
            optimal_actions.append(option)

        for tuple in optimal_actions:
            minimum = min(optimal_actions)
            if tuple[0] == minimum[0]:
                results.append(tuple[1])

    # return random choice
    return random.choice(results)


def max_value(board):

    if terminal(board):
        return utility(board)

    # Recurise function for max value, compare actual V_Max to opposite player
    V_max = -math.inf
    for action in actions(board):
        V_max = max(V_max, min_value(result(board, action)))
    return V_max


def min_value(board):

    if terminal(board):
        return utility(board)

    V_min = math.inf
    for action in actions(board):
        V_min = min(V_min, max_value(result(board, action)))
    return V_min
