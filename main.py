import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

root = tk.Tk()
root.title("Tic Tac Toe")

b = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]]
game_board = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]]

human_wins = 0
ai_wins = 0
draws = 0
player_symbol = "X"
ai_symbol = "O"
player_turn = True
counter = 0
current_algorithm = 0

config_frame = tk.Frame(root)
config_frame.grid(row=0, column=3, rowspan=3, padx=10, sticky="n")

def Winner(board):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != " ":
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]
    return None

def make_ai_move():
    global player_turn, counter
    move = best_move(game_board)

    if move:
        row, col = move
        game_board[row][col] = ai_symbol
        b[row][col].config(text=ai_symbol)
        player_turn = True
        counter += 1
        winner = Winner(game_board)
        if winner == ai_symbol:
            messagebox.showinfo("Tic Tac Toe", "AI won!")
            reset()
            return
        elif counter == 9:
            messagebox.showinfo("Tic Tac Toe", "It's a draw!")
            reset()
            return

def reset(new_game=False):
    global game_board, player_turn, counter, human_wins, ai_wins, draws
    if not new_game:
        winner = Winner(game_board)
        if winner == player_symbol:
            human_wins += 1
            human_wins_label.config(text=f"Human Wins: {human_wins}")
        elif winner == ai_symbol:
            ai_wins += 1
            ai_wins_label.config(text=f"AI Wins: {ai_wins}")
        elif counter == 9:
            draws += 1
            draws_label.config(text=f"Draws: {draws}")

    counter = 0
    for row in range(3):
        for col in range(3):
            game_board[row][col] = " "
            b[row][col].config(text=" ")

    player_turn = (player_symbol == "X")
    if not player_turn and not new_game:
        root.after(100, make_ai_move)

def start_game():
    global current_algorithm, player_symbol, ai_symbol
    current_algorithm = algorithm_var.get()
    player_symbol = player_var.get()
    ai_symbol = "O" if player_symbol == "X" else "X"
    reset()

algorithm_label = tk.Label(config_frame, text="Select Algorithm:")
algorithm_label.grid(row=0, column=0, sticky="w", pady=(10, 0))
algorithm_var = tk.IntVar(value=0)
algorithms = ["Simple Minimax",
              "Minimax with Alpha-Beta Pruning",
              "Minimax with Greedy Best-First",
              "Minimax with A*",
              "Minimax with Symmetry Reduction",
              "Minimax with Heuristic Reduction"]

def on_algorithm_change(*args):
    start_game()

algorithm_var.trace("w", on_algorithm_change)
for i, algo_name in enumerate(algorithms):
    tk.Radiobutton(config_frame, text=algo_name, variable=algorithm_var, value=i).grid(
        row=i+1, column=0, sticky="w")

player_label = tk.Label(config_frame, text="Starting Player:")
player_label.grid(row=7, column=0, sticky="w", pady=(10, 0))
player_var = tk.StringVar(value="X")

def on_player_change(*args):
    start_game()

player_var.trace("w", on_player_change)
tk.Radiobutton(config_frame, text="Player (X)", variable=player_var, value="X").grid(
    row=8, column=0, sticky="w")
tk.Radiobutton(config_frame, text="AI (O)", variable=player_var, value="O").grid(
    row=9, column=0, sticky="w")

stats_frame = tk.LabelFrame(config_frame, text="Statistics")
stats_frame.grid(row=10, column=0, pady=10, sticky="ew")
human_wins_label = tk.Label(stats_frame, text="Human Wins: 0")
human_wins_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
ai_wins_label = tk.Label(stats_frame, text="AI Wins: 0")
ai_wins_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
draws_label = tk.Label(stats_frame, text="Draws: 0")
draws_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)

def minimax_simple(board, depth, is_maximizing):
    winner = Winner(board)
    if winner == player_symbol:
        return -10
    elif winner == ai_symbol:
        return 10
    elif all(cell != " " for row in board for cell in row):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = ai_symbol
                    score = minimax_simple(board, depth + 1, False)
                    board[row][col] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = player_symbol
                    score = minimax_simple(board, depth + 1, True)
                    board[row][col] = " "
                    best_score = min(score, best_score)
        return best_score
def minimax_alpha_beta(board, depth, is_maximizing, alpha, beta):
    winner = Winner(board)
    if winner == player_symbol:
        return -10
    elif winner == ai_symbol:
        return 10
    elif all(cell != " " for row in board for cell in row):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = ai_symbol
                    score = minimax_alpha_beta(board, depth + 1, False, alpha, beta)
                    board[row][col] = " "
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if alpha >= beta:
                        return alpha
        return best_score
    else:
        best_score = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = player_symbol
                    score = minimax_alpha_beta(board, depth + 1, True, alpha, beta)
                    board[row][col] = " "
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if alpha >= beta:
                        return beta
        return best_score

def heuristic_h(board, player):
    opponent = player_symbol if player == ai_symbol else ai_symbol
    score = 0
    lines = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]
    for line in lines:
        if opponent not in line:
            score += 1
    return score

def minimax_greedy(board, depth, is_maximizing):
    winner = Winner(board)
    if winner == player_symbol:
        return -10 + depth
    elif winner == ai_symbol:
        return 10 - depth
    elif all(cell != " " for row in board for cell in row):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = ai_symbol
                    score = minimax_greedy(board, depth + 1, False) + heuristic_h(board, ai_symbol)
                    board[row][col] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = player_symbol
                    score = minimax_greedy(board, depth + 1, True) - heuristic_h(board, player_symbol)
                    board[row][col] = " "
                    best_score = min(score, best_score)
        return best_score

def heuristic_astar(board):
    score = 0
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]

    b2 = [board[row][col] for row in range(3) for col in range(3)]

    for (a, b, c) in win_conditions:
        if b2[a] == b2[b] == player_symbol and b2[c] == " ":
            score += 10
        elif b2[b] == b2[c] == player_symbol and b2[a] == " ":
            score += 10
        elif b2[a] == b2[c] == player_symbol and b2[b] == " ":
            score += 10

        elif b2[a] == b2[b] == ai_symbol and b2[c] == " ":
            score -= 10
        elif b2[b] == b2[c] == ai_symbol and b2[a] == " ":
            score -= 10
        elif b2[a] == b2[c] == ai_symbol and b2[b] == " ":
            score -= 10
    return score

def minimax_astar(board, depth, is_maximizing):
    winner = Winner(board)
    if winner == ai_symbol:
        return 10
    elif winner == player_symbol:
        return -10
    elif all(cell != " " for row in board for cell in row):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = ai_symbol
                    score = heuristic_astar(board) + minimax_astar(board, depth + 1, False)
                    board[row][col] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = player_symbol
                    score = heuristic_astar(board) + minimax_astar(board, depth + 1, True)
                    board[row][col] = " "
                    best_score = min(score, best_score)
        return best_score

memo = {}

def rotate_board(board):
    return [list(reversed(col)) for col in zip(*board)]

def reflect_board(board):
    return [list(reversed(row)) for row in board]

def get_canonical_board(board):
    transformations = [board,
                       rotate_board(board),
                       rotate_board(rotate_board(board)),
                       rotate_board(rotate_board(rotate_board(board))),
                       reflect_board(board),
                       rotate_board(reflect_board(board)),
                       rotate_board(rotate_board(reflect_board(board))),
                       rotate_board(rotate_board(rotate_board(reflect_board(board))))]
    return min(tuple(tuple(row) for row in b) for b in transformations)

def minimax_symmetry(board, depth, is_maximizing):
    canonical_board = get_canonical_board(board)
    board_tuple = tuple(tuple(row) for row in canonical_board)
    if board_tuple in memo:
        return memo[board_tuple]
    winner = Winner(board)
    if winner == ai_symbol:
        return 10
    elif winner == player_symbol:
        return -10
    elif all(cell != " " for row in board for cell in row):
        return 0

    best_score = -float("inf") if is_maximizing else float("inf")
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = ai_symbol if is_maximizing else player_symbol
                score = minimax_symmetry(board, depth + 1, not is_maximizing)
                board[row][col] = " "
                best_score = max(score, best_score) if is_maximizing else min(score, best_score)
    memo[board_tuple] = best_score
    return best_score

def heuristic_reduction(board):
    score = 0
    for row in range(3):
        x_count = board[row].count(player_symbol)
        o_count = board[row].count(ai_symbol)
        if o_count == 2 and x_count == 0:
            score += 10
        elif x_count == 2 and o_count == 0:
            score -= 10
    for col in range(3):
        column = [board[0][col], board[1][col], board[2][col]]
        x_count = column.count(player_symbol)
        o_count = column.count(ai_symbol)
        if o_count == 2 and x_count == 0:
            score += 10
        elif x_count == 2 and o_count == 0:
            score -= 10
    diagonals = [[board[0][0], board[1][1], board[2][2]],
                 [board[0][2], board[1][1], board[2][0]]]
    for diag in diagonals:
        x_count = diag.count(player_symbol)
        o_count = diag.count(ai_symbol)
        if o_count == 2 and x_count == 0:
            score += 10
        elif x_count == 2 and o_count == 0:
            score -= 10
    return score

def minimax_heuristic_reduction(board, depth, is_maximizing):
    winner = Winner(board)
    if winner == player_symbol:
        return -100
    elif winner == ai_symbol:
        return 100
    elif all(cell != " " for row in board for cell in row):
        return 0

    if depth >= 2:
        return heuristic_reduction(board)

    if is_maximizing:
        best_score = -float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = ai_symbol
                    score = minimax_heuristic_reduction(board, depth + 1, False)
                    board[row][col] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = player_symbol
                    score = minimax_heuristic_reduction(board, depth + 1, True)
                    board[row][col] = " "
                    best_score = min(score, best_score)
        return best_score

def best_move(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = ai_symbol
                if Winner(board) == ai_symbol:
                    board[row][col] = " "
                    return (row, col)
                board[row][col] = " "
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = player_symbol
                if Winner(board) == player_symbol:
                    board[row][col] = " "
                    return (row, col)
                board[row][col] = " "

    best_score = -float("inf")
    move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = ai_symbol

                if current_algorithm == 0:
                    score = minimax_simple(board, 0, False)
                elif current_algorithm == 1:
                    score = minimax_alpha_beta(board, 0, False, -float('inf'), float('inf'))
                elif current_algorithm == 2:
                    score = minimax_greedy(board, 0, False) + heuristic_h(board, ai_symbol)
                elif current_algorithm == 3:
                    score = minimax_astar(board, 0, False)
                elif current_algorithm == 4:
                    score = minimax_symmetry(board, 0, False)
                elif current_algorithm == 5:
                    score = heuristic_reduction(board) + minimax_heuristic_reduction(board, 0, False)

                board[row][col] = " "
                if score > best_score:
                    best_score = score
                    move = (row, col)
    return move

def b_click(button, row, col):
    global player_turn, counter
    if button["text"] == " " and player_turn:
        game_board[row][col] = player_symbol
        button.config(text=player_symbol)
        player_turn = False
        counter += 1
        winner = Winner(game_board)
        if winner == player_symbol:
            messagebox.showinfo("Tic Tac Toe", "Human won!")
            reset()
            return
        elif counter == 9:
            messagebox.showinfo("Tic Tac Toe", "It's a draw!")
            reset()
            return

        root.after(100, make_ai_move)
    elif not player_turn:
        messagebox.showinfo("Tic Tac Toe", "Wait for AI's move")
    else:
        messagebox.showerror("Tic Tac Toe", "This cell is already taken!")

for row in range(3):
    for col in range(3):
        b[row][col] = tk.Button(root, text=" ", font=("Arial", 26), height=3, width=5, bg="White",command=lambda r=row, c=col: b_click(b[r][c], r, c))
        b[row][col].grid(row=row, column=col)

start_game()
root.mainloop()

results = ["Human Wins", "AI Wins", "Draws"]
counts = [human_wins, ai_wins, draws]

plt.bar(results, counts, color=["blue", "red", "green"])
plt.xlabel("Outcome")
plt.ylabel("Count")
plt.title("Tic Tac Toe Game Outcomes")
plt.show()