import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O

def actions(board):
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves

def result(board, action):
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception("Invalid move: Cell is already occupied.")
    
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None

def terminal(board):
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)

def utility(board):
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def minimax(board):
    if terminal(board):
        return None

    turn = player(board)

    if turn == X:
        best_score = float('-inf')
        best_move = None
        for action in actions(board):
            move_score = min_value(result(board, action))
            if move_score > best_score:
                best_score = move_score
                best_move = action
    else:
        best_score = float('inf')
        best_move = None
        for action in actions(board):
            move_score = max_value(result(board, action))
            if move_score < best_score:
                best_score = move_score
                best_move = action

    return best_move

def max_value(board):
    if terminal(board):
        return utility(board)
    
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
