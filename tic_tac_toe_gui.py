"""
Tic-Tac-Toe Game AI — GUI Version (Tkinter)
=============================================
Click-to-play graphical version of the Minimax-powered Tic-Tac-Toe AI.
You play as X, the AI plays as O and moves automatically after you.

Run with:  python3 tic_tac_toe_gui.py
(Tkinter ships with standard Python installs, no extra packages needed.)
"""

import math
import tkinter as tk
from tkinter import messagebox

HUMAN = "X"
AI = "O"
EMPTY = ""

WIN_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def check_winner(board):
    for a, b, c in WIN_COMBOS:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    if EMPTY not in board:
        return "Draw"
    return None


def minimax(board, depth, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner == AI:
        return 10 - depth
    elif winner == HUMAN:
        return depth - 10
    elif winner == "Draw":
        return 0

    if is_maximizing:
        best = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                best = max(best, minimax(board, depth + 1, False, alpha, beta))
                board[i] = EMPTY
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = HUMAN
                best = min(best, minimax(board, depth + 1, True, alpha, beta))
                board[i] = EMPTY
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best


def best_ai_move(board):
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = AI
            score = minimax(board, 0, False, -math.inf, math.inf)
            board[i] = EMPTY
            if score > best_score:
                best_score = score
                move = i
    return move


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe — Minimax AI")
        self.root.resizable(False, False)
        self.board = [EMPTY] * 9
        self.buttons = []
        self.game_over = False

        header = tk.Label(root, text="You are X — AI is O", font=("Helvetica", 14, "bold"))
        header.grid(row=0, column=0, columnspan=3, pady=10)

        for i in range(9):
            btn = tk.Button(
                root, text=EMPTY, font=("Helvetica", 32, "bold"),
                width=4, height=2,
                command=lambda i=i: self.human_click(i)
            )
            btn.grid(row=1 + i // 3, column=i % 3, padx=3, pady=3)
            self.buttons.append(btn)

        restart_btn = tk.Button(root, text="Restart Game", font=("Helvetica", 12),
                                 command=self.restart)
        restart_btn.grid(row=4, column=0, columnspan=3, pady=10)

    def human_click(self, i):
        if self.game_over or self.board[i] != EMPTY:
            return

        self.board[i] = HUMAN
        self.buttons[i].config(text=HUMAN, fg="#2563eb")

        if self.end_check():
            return

        # AI's turn
        self.root.after(300, self.ai_move)

    def ai_move(self):
        move = best_ai_move(self.board)
        if move is not None:
            self.board[move] = AI
            self.buttons[move].config(text=AI, fg="#dc2626")
        self.end_check()

    def end_check(self):
        result = check_winner(self.board)
        if result:
            self.game_over = True
            if result == "Draw":
                messagebox.showinfo("Game Over", "It's a draw!")
            elif result == HUMAN:
                messagebox.showinfo("Game Over", "You win! (Minimax AI let its guard down? Try again!)")
            else:
                messagebox.showinfo("Game Over", "The AI wins!")
            return True
        return False

    def restart(self):
        self.board = [EMPTY] * 9
        self.game_over = False
        for btn in self.buttons:
            btn.config(text=EMPTY)


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
