# Task List: Project 1 Part 3

- [x] Task 1: Environment & Baseline Files (`pyproject.toml`, `.python-version`, `model.py`)
  - Acceptance: `uv sync` succeeds in `project_3/` with Python 3.11 and Pygame.
  - Verify: `uv run python -c "import pygame; print(pygame.__version__)"`
  - Files: `project_3/pyproject.toml`, `project_3/.python-version`, `project_3/model.py`

- [x] Task 2: Figure 7 Board Encoding (`levels.py`)
  - Acceptance: Figure 7 Examples 1 & 2 match the PDF diagrams exactly.
  - Verify: Visual inspection of grid strings and counts of boxes/targets/walls.
  - Files: `project_3/levels.py`

- [x] Task 3: Deadlock Detection Engine (`deadlocks.py`, `test_deadlocks.py`)
  - Acceptance: Corner and Line deadlocks match the red and yellow positions in Figures 5 & 6.
  - Verify: `uv run python -m unittest test_deadlocks.py` passes all assertions.
  - Files: `project_3/deadlocks.py`, `project_3/test_deadlocks.py`

- [x] Task 4: Search Engines with Hard Pruning (`heuristics.py`, `search.py`)
  - Acceptance: `Improved_A_Star` discards deadlocked successors before queue insertion.
  - Verify: Improved A* yields the same optimal cost as BFS/Standard A* with fewer explored nodes.
  - Files: `project_3/heuristics.py`, `project_3/search.py`

- [x] Task 5: Interactive CLI & Comparison Benchmark (`main.py`)
  - Acceptance: Flat level selection (1–7), option to run individual algorithms or benchmark comparison.
  - Verify: Terminal execution runs and displays side-by-side metrics table.
  - Files: `project_3/main.py`

- [x] Task 6: GUI Visualizer Adaptation (`gui.py`)
  - Acceptance: Pygame GUI loads Figure 7 mazes with start button, 1.0s pacing, shadows, and telemetry.
  - Verify: Launch GUI on Example 1 and step through moves.
  - Files: `project_3/gui.py`

- [x] Task 7: Comprehensive Master Documentation (`README.md`)
  - Acceptance: Complete Part 3 guide explaining deadlocks, pruning, benchmarks, and FAQ.
  - Verify: Review `README.md` completeness and confirm zero comments in `.py` source files.
  - Files: `project_3/README.md`
