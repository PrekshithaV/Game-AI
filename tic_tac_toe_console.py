"""
Tic-Tac-Toe Game AI
====================
A console-based Tic-Tac-Toe game featuring an unbeatable AI opponent
built using the Minimax algorithm with Alpha-Beta Pruning.

Modes supported:
    1. Human vs AI (Hard - Minimax, unbeatable)
    2. Human vs AI (Easy - Random moves)
    3. AI vs AI (watch two Minimax agents play)

Author: (your name here)
"""

import math
import random
import time

HUMAN = "X"
AI = "O"
EMPTY = " "


class TicTacToe:
    def __init__(self):
        # Board positions are indexed 0-8, left to right, top to bottom
        self.board = [EMPTY] * 9

    def print_board(self):
        b = self.board
        print()
        print(f" {b[0]} | {b[1]} | {b[2]} ")
        print("---+---+---")
        print(f" {b[3]} | {b[4]} | {b[5]} ")
        print("---+---+---")
        print(f" {b[6]} | {b[7]} | {b[8]} ")
        print()

    def available_moves(self):
        return [i for i, v in enumerate(self.board) if v == EMPTY]

    def make_move(self, pos, player):
        if self.board[pos] == EMPTY:
            self.board[pos] = player
            return True
        return False

    def undo_move(self, pos):
        self.board[pos] = EMPTY

    def check_winner(self):
        """Returns 'X', 'O', 'Draw', or None (game still going)."""
        win_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
            (0, 4, 8), (2, 4, 6)               # diagonals
        ]
        for a, b, c in win_combinations:
            if self.board[a] != EMPTY and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]

        if EMPTY not in self.board:
            return "Draw"

        return None

    def is_game_over(self):
        return self.check_winner() is not None


# ---------------------------------------------------------------------------
# THE AI AGENT
# ---------------------------------------------------------------------------
class MinimaxAgent:
    """
    An unbeatable Tic-Tac-Toe agent using Minimax with Alpha-Beta Pruning.

    How it works:
    --------------
    - The AI simulates every possible future sequence of moves from the
      current board state.
    - It assumes the opponent (human) will always play optimally too.
    - It assigns a score to each terminal (end) state:
          AI win    -> +10 - depth   (win sooner = higher score)
          Human win -> depth - 10    (lose later = less negative)
          Draw      ->  0
    - It picks the move that MAXIMIZES its guaranteed outcome, assuming
      the opponent will always try to MINIMIZE it. Hence "Minimax".
    - Alpha-Beta Pruning cuts off branches that can't possibly change the
      final decision, making the search much faster without changing
      the result.
    """

    def __init__(self, player_symbol, opponent_symbol):
        self.player = player_symbol
        self.opponent = opponent_symbol

    def best_move(self, game: TicTacToe):
        best_score = -math.inf
        move = None
        for pos in game.available_moves():
            game.make_move(pos, self.player)
            score = self._minimax(game, depth=0, is_maximizing=False,
                                   alpha=-math.inf, beta=math.inf)
            game.undo_move(pos)
            if score > best_score:
                best_score = score
                move = pos
        return move

    def _minimax(self, game, depth, is_maximizing, alpha, beta):
        winner = game.check_winner()
        if winner == self.player:
            return 10 - depth
        elif winner == self.opponent:
            return depth - 10
        elif winner == "Draw":
            return 0

        if is_maximizing:
            best = -math.inf
            for pos in game.available_moves():
                game.make_move(pos, self.player)
                best = max(best, self._minimax(game, depth + 1, False, alpha, beta))
                game.undo_move(pos)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break  # Alpha-Beta pruning
            return best
        else:
            best = math.inf
            for pos in game.available_moves():
                game.make_move(pos, self.opponent)
                best = min(best, self._minimax(game, depth + 1, True, alpha, beta))
                game.undo_move(pos)
                beta = min(beta, best)
                if beta <= alpha:
                    break  # Alpha-Beta pruning
            return best


class RandomAgent:
    """A simple 'Easy' difficulty AI that just picks a random valid move."""

    def __init__(self, player_symbol):
        self.player = player_symbol

    def best_move(self, game: TicTacToe):
        return random.choice(game.available_moves())


# ---------------------------------------------------------------------------
# GAME LOOP / MODES
# ---------------------------------------------------------------------------
def human_move(game: TicTacToe):
    while True:
        try:
            pos = int(input("Enter your move (1-9, left to right/top to bottom): ")) - 1
            if pos not in range(9):
                print("Please enter a number between 1 and 9.")
                continue
            if game.board[pos] != EMPTY:
                print("That cell is already taken. Try again.")
                continue
            return pos
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")


def play_human_vs_ai(difficulty="hard"):
    game = TicTacToe()
    ai = MinimaxAgent(AI, HUMAN) if difficulty == "hard" else RandomAgent(AI)

    print("\nYou are 'X'. The AI is 'O'.")
    print("Board positions are numbered 1-9:")
    print(" 1 | 2 | 3 \n 4 | 5 | 6 \n 7 | 8 | 9 ")
    game.print_board()

    current = HUMAN
    while not game.is_game_over():
        if current == HUMAN:
            pos = human_move(game)
            game.make_move(pos, HUMAN)
        else:
            print("AI is thinking...")
            time.sleep(0.4)
            pos = ai.best_move(game)
            game.make_move(pos, AI)
            print(f"AI plays position {pos + 1}")

        game.print_board()
        current = AI if current == HUMAN else HUMAN

    result = game.check_winner()
    if result == "Draw":
        print("It's a draw!")
    elif result == HUMAN:
        print("Congratulations, you win!")
    else:
        print("The AI wins!")


def play_ai_vs_ai():
    game = TicTacToe()
    agent_x = MinimaxAgent(HUMAN, AI)
    agent_o = MinimaxAgent(AI, HUMAN)

    game.print_board()
    current = HUMAN
    while not game.is_game_over():
        agent = agent_x if current == HUMAN else agent_o
        pos = agent.best_move(game)
        game.make_move(pos, current)
        print(f"{current} plays position {pos + 1}")
        game.print_board()
        time.sleep(0.5)
        current = AI if current == HUMAN else HUMAN

    result = game.check_winner()
    print("It's a draw!" if result == "Draw" else f"{result} wins!")


def main():
    print("=" * 50)
    print("        TIC-TAC-TOE  —  GAME AI PROJECT")
    print("=" * 50)
    print("1. Play vs AI (Hard - Unbeatable Minimax)")
    print("2. Play vs AI (Easy - Random)")
    print("3. Watch AI vs AI")
    print("4. Exit")

    choice = input("Choose an option (1-4): ").strip()
    if choice == "1":
        play_human_vs_ai("hard")
    elif choice == "2":
        play_human_vs_ai("easy")
    elif choice == "3":
        play_ai_vs_ai()
    else:
        print("Goodbye!")


if __name__ == "__main__":
    main()
