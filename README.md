# Game AI Project — Tic-Tac-Toe with Minimax

An AI agent that plays Tic-Tac-Toe against a human or against itself,
using the **Minimax algorithm with Alpha-Beta Pruning** to play perfectly
(it never loses).

---

## 1. Project Overview

| | |
|---|---|
| **Game** | Tic-Tac-Toe (3x3 grid) |
| **AI Technique** | Minimax algorithm + Alpha-Beta Pruning |
| **Language** | Python 3 |
| **Interfaces** | Console (text) and GUI (Tkinter) |
| **Modes** | Human vs AI, Easy AI (random) vs Human, AI vs AI |

### Why Tic-Tac-Toe + Minimax?
Tic-Tac-Toe has a small enough state space (at most 9! = 362,880 possible
game sequences) that a full game-tree search is feasible in real time.
This makes it the standard first project for demonstrating **adversarial
search** — the same family of algorithms used in Chess and Checkers
engines, just at a much smaller scale.

---

## 2. How the AI Works (Algorithm Explanation)

### The Minimax Algorithm
Minimax is a decision-making algorithm used in two-player, turn-based,
zero-sum games (one player's win is the other's loss).

The core idea:
- The AI (MAX) wants to **maximize** its score.
- The opponent (MIN) is assumed to always play optimally, i.e. trying to
  **minimize** the AI's score.
- The algorithm explores every possible sequence of future moves,
  building a game tree, until it reaches an end state (win, loss, or draw).
- Each end state gets a score:
  - AI wins → **+10 − depth** (winning sooner is scored higher)
  - Human wins → **depth − 10** (losing later is scored less negative)
  - Draw → **0**
- The algorithm works backward up the tree: at MAX levels it picks the
  highest score among children; at MIN levels it picks the lowest.
- The AI then plays the move that leads to the branch with the best
  guaranteed outcome, assuming perfect play from the opponent.

This is why the Hard AI is **unbeatable** — the best a human can achieve
against it is a draw.

### Alpha-Beta Pruning
A plain Minimax search on Tic-Tac-Toe is already fast, but Alpha-Beta
Pruning is included to demonstrate the standard optimization used in
real game engines (including Chess AIs). It keeps two values, alpha
(best score MAX can guarantee) and beta (best score MIN can guarantee),
and **cuts off branches that can't possibly affect the final decision**,
since a rational opponent would never allow the AI to reach them. This
reduces the number of nodes evaluated without changing the outcome.

### Easy Mode
A `RandomAgent` class is included that just picks any available cell.
This gives you a "beatable" difficulty to contrast against the Minimax
agent, and is a nice talking point in a project demo/viva: you can show
both a naive AI and an optimal AI side by side.

---

## 3. Files Included

```
game_ai_project/
├── tic_tac_toe_console.py   # Console version: Human vs AI, AI vs AI, Easy/Hard modes
├── tic_tac_toe_gui.py       # GUI version (Tkinter): click-to-play against Minimax AI
└── README.md                # This file
```

---

## 4. Requirements

- Python 3.7 or later (no external libraries needed — everything used
  is part of Python's standard library: `math`, `random`, `time`,
  `tkinter`).
- Tkinter usually ships with Python by default. If it's missing on
  Linux, install it with:
  ```bash
  sudo apt-get install python3-tk
  ```

---

## 5. Step-by-Step Execution

### Option A: Console Version
1. Open a terminal and navigate to the project folder:
   ```bash
   cd game_ai_project
   ```
2. Run the script:
   ```bash
   python3 tic_tac_toe_console.py
   ```
3. Choose a mode from the menu:
   - `1` → Play against the unbeatable Hard AI
   - `2` → Play against the Easy (random) AI
   - `3` → Watch two Hard AIs play each other (always ends in a draw)
   - `4` → Exit
4. If playing, enter a number **1–9** corresponding to the board position:
   ```
    1 | 2 | 3
    4 | 5 | 6
    7 | 8 | 9
   ```

### Option B: GUI Version
1. Navigate to the project folder:
   ```bash
   cd game_ai_project
   ```
2. Run the script:
   ```bash
   python3 tic_tac_toe_gui.py
   ```
3. A window opens with a 3x3 grid of buttons. Click any empty cell to
   place your `X`. The AI (`O`) will respond automatically after a
   short delay.
4. Click **Restart Game** at any point to reset the board.

---

## 6. How to Extend This Project (Ideas for Improvement)

If you want to build on this for a more advanced submission:
- **Add a scoreboard** that tracks wins/losses/draws across multiple rounds.
- **Add difficulty levels to the GUI** (currently the GUI only uses Hard mode).
- **Move to a 4x4 or Connect-4 board** and add a **depth-limited Minimax
  with a heuristic evaluation function**, since full-depth search
  becomes too slow on larger boards — this is exactly the technique
  real Chess engines use.
- **Add Chess** as a stretch goal using the `python-chess` library for
  move generation/validation, combined with a heuristic Minimax
  (material count + positional tables) since full-game-tree search is
  computationally infeasible for Chess.

---

## 7. Sample Output (Console, AI vs AI)

```
X plays position 1
O plays position 5
X plays position 2
O plays position 3
...
It's a draw!
```

This confirms the Minimax agent plays optimally — when two perfect
players face off, the mathematically correct outcome of Tic-Tac-Toe is
always a draw.
