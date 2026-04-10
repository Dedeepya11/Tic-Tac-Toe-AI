from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Check winner
def check_winner(board):
    win_states = [
        [0,1,2],[3,4,5],[6,7,8],  # rows
        [0,3,6],[1,4,7],[2,5,8],  # cols
        [0,4,8],[2,4,6]           # diagonals
    ]
    for state in win_states:
        if board[state[0]] == board[state[1]] == board[state[2]] and board[state[0]] != "":
            return board[state[0]]
    if "" not in board:
        return "draw"
    return None

# Minimax algorithm
def minimax(board, is_maximizing):
    winner = check_winner(board)

    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif winner == "draw":
        return 0

    if is_maximizing:
        best_score = -100
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = 100
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, True)
                board[i] = ""
                best_score = min(score, best_score)
        return best_score

# AI move
def best_move(board):
    best_score = -100
    move = 0
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    board = request.json["board"]

    # AI plays
    ai_move = best_move(board)
    board[ai_move] = "O"

    winner = check_winner(board)

    return jsonify({
        "board": board,
        "winner": winner
    })

if __name__ == "__main__":
    app.run(debug=True)