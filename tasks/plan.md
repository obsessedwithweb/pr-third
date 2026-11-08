# Implementation Plan: Project 1 Part 3

## 1. Objectives & Architectural Components
* **Module 1: Environment & Dependency Setup** (`pyproject.toml`, `.python-version`)
  - Pin Python 3.11 and Pygame 2.6.1 with `uv`.
* **Module 2: Board Encodings** (`levels.py`)
  - Encode Figure 7 (Ex 1 & Ex 2) pixel-accurately from PDF inspection.
  - Include Figure 4 (Ex 1–5) for backward comparison.
* **Module 3: Core Model** (`model.py`)
  - `SokobanPuzzle` and `Node` (inherited from project_2, comment-free).
* **Module 4: Deadlock Engine** (`deadlocks.py`)
  - Static detection of corner deadlocks (perpendicular walls).
  - Static detection of line deadlocks (unbroken wall segments between corners with zero targets).
  - Runtime check `is_deadlock(state, static_deadlocks)`.
* **Module 5: Heuristics & Search Engines** (`heuristics.py`, `search.py`)
  - Standard A* ($h_1, h_2, h_3$) and BFS.
  - `Improved_A_Star`: skips successors immediately when `is_deadlock()` is True.
* **Module 6: Verification & Benchmarking** (`test_deadlocks.py`, `main.py`)
  - Unit test verifying exact match with red/yellow dots in Figures 5 & 6.
  - Interactive CLI with flat level list (1–7) and comparison mode.
* **Module 7: GUI & Master Documentation** (`gui.py`, `README.md`)
  - Modern Pygame interface for Figure 7 levels.
  - Complete Part 3 guide in `README.md`.

## 2. Implementation Order
1. Environment (`pyproject.toml`, `levels.py`, `model.py`)
2. Deadlocks Engine (`deadlocks.py`, `test_deadlocks.py`)
3. Search with Pruning (`heuristics.py`, `search.py`)
4. CLI & GUI (`main.py`, `gui.py`)
5. Benchmarking & Documentation (`README.md`)
