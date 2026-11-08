# Spec: Sokoban Solver — Project 1 Part 3 (Deadlock Detection & Search Pruning)

## Objective
Implement **Part 3** of the Sokoban project in a dedicated `project_3/` directory using `uv`. 
The core objective is to detect unplaced box **deadlocks** (Corner and Line deadlocks), integrate deadlock detection into the A* search algorithm via **hard pruning** (preventing doomed branches from being expanded or added to the priority queue), benchmark on the new Figure 7 levels, and compare with the previous algorithms (BFS and unpruned A* with $h_1, h_2, h_3$). An updated Pygame GUI will visualize the solutions for the new Figure 7 board layouts.

---

## Tech Stack
* **Runtime:** Python 3.11 (pinned via `.python-version`)
* **Environment & Package Manager:** `uv` (`pyproject.toml` with `[tool.uv] package = false`)
* **Libraries:** `pygame==2.6.1`
* **Standard Library:** `collections.deque`, `heapq`, `time`, `copy`

---

## Commands
* **Run interactive CLI & GUI:**
  ```bash
  cd "/home/rma/Studies/M1/Problems Resolution/project_3"
  uv run python main.py
  ```
* **Run automated verification tests:**
  ```bash
  uv run python -m unittest test_deadlocks.py
  ```

---

## Project Structure
```
project_3/
├── pyproject.toml        # Project dependencies and uv configuration
├── .python-version       # Python 3.11 runtime pin
├── SPEC.md               # This formal specification
├── README.md             # Comprehensive Part 3 guide (theory, line deadlocks, comparison)
├── model.py              # SokobanPuzzle and Node classes (comment-free)
├── deadlocks.py          # Static and dynamic deadlock detection (Corner & Line)
├── heuristics.py         # Heuristic functions h1, h2, h3 (comment-free)
├── search.py             # BFS, Standard A*, and Improved A* with hard pruning (comment-free)
├── levels.py             # Figure 7 (Examples 1 & 2) and Figure 4 (Examples 1 to 5)
├── gui.py                # Pygame simulation studio adapted for Figure 7 mazes
└── main.py               # Interactive CLI for algorithm comparison and GUI execution
```

---

## Code Style & Conventions
* **Strict Zero-Comments Policy:** All Python source files (`.py`) must contain **no comments and no docstrings**.
* **Documentation Location:** All mathematical formulas, explanations, deadlocks theory, and architecture must reside in `README.md`.
* **Code formatting:** Clean, readable, idiomatic Python using descriptive variable names.
* **Example Style:**
  ```python
  def is_deadlock_state(puzzle, static_deadlocks):
      for r, c in puzzle.get_unplaced_boxes():
          if (r, c) in static_deadlocks:
              return True
      return False
  ```

---

## Key Technical Specifications for Part 3

### 1. Deadlock Detection (`deadlocks.py`)
* **Corner Deadlock:** A non-target floor tile bounded by two perpendicular walls (North+East, North+West, South+East, South+West).
* **Line Deadlock:** A row or column of non-target floor tiles bounded on one side entirely by a flat wall segment connecting two corner deadlocks, with no storage target along the segment and no lateral exit/opening.
* **Precomputed Static Deadlock Map:**
  * When a board is loaded, all non-target tiles that are corner or line deadlocks are identified once and stored in a `set` of coordinates `(r, c)`.
  * Runtime deadlock check becomes an instantaneous $O(1)$ set lookup per unplaced box:
    ```python
    any((r, c) in static_deadlocks for (r, c) in puzzle.get_unplaced_boxes())
    ```

### 2. Improved A* Search with Hard Pruning (`search.py`)
* In the search expansion loop:
  ```python
  for action, successor in current_node.state.successorFunction():
      if is_deadlock_state(successor, static_deadlocks):
          continue  # Prune branch: do not create Node, do not compute h, do not push to Open
  ```

### 3. Figure 7 Levels Encoding (`levels.py`)
* **Figure 7 — Example 1:** 7x7 warehouse, 3 boxes, 3 targets, vertical central pillar with bottleneck passage.
* **Figure 7 — Example 2:** Irregular warehouse, 4 boxes, 4 targets, perimeter line-deadlock walls.
* **Figure 4 Levels (1 to 5):** Preserved for backwards compatibility and benchmarking.

### 4. Interactive CLI & Comparative Benchmarking (`main.py`)
* Option to select Figure 7 levels or Figure 4 levels.
* Option to run:
  1. BFS
  2. Standard A* ($h_1, h_2, h_3$)
  3. **Improved A* ($h_3$ + Deadlock Pruning)**
  4. **Run Benchmark Comparison:** Executes all algorithms on the selected level and displays a side-by-side comparison table of explored nodes, cost, and time.

---

## Testing Strategy
* `test_deadlocks.py`: Self-contained unit tests verifying:
  1. All red tiles in Figure 5 are correctly identified as Corner Deadlocks.
  2. All yellow tiles in Figure 6 are correctly identified as Line Deadlocks.
  3. Storage target tiles are never marked as deadlocks.
  4. Improved A* returns the optimal solution while exploring fewer or equal nodes compared to Standard A*.

---

## Boundaries
* **Always:**
  * Use `uv` for environment and package management.
  * Keep source code completely comment-free.
  * Document all theory, line deadlock mechanics, and comparison tables in `README.md`.
* **Ask First:**
  * Introducing external libraries beyond Pygame.
  * Modifying problem formulation constants (`O`, `R`, `B`, `S`, etc.).
* **Never:**
  * Use heuristic soft penalty (+1000) as a replacement for hard pruning in Part 3.
  * Hardcode solution moves or level dimensions.

---

## Success Criteria
1. `is_deadlock()` correctly identifies all corner and line deadlocks on Figure 7 Examples 1 and 2.
2. Improved A* finds the optimal solution on both Figure 7 levels without exploring deadlocked subtrees.
3. Node count and time for Improved A* ($h_3$ + pruning) are measured and compared against BFS and standard A*.
4. Pygame GUI correctly loads, displays, and animates Figure 7 levels with the modern aesthetic (1.0s delay, shadows, gradients, telemetry).
5. Comprehensive `README.md` is authored, explaining all new concepts introduced in Part 3.

---

## Open Questions & Clarifications
1. **Board Selection Menu:** In the CLI, do you prefer a unified menu showing both Figure 7 levels and Figure 4 levels (e.g., Level 1–5 for Fig 4, Level 6–7 for Fig 7), or a sub-menu asking *"Select set: 1) Figure 7 (New) 2) Figure 4 (Old)"*?
2. **Dynamic Box-on-Box Deadlocks:** Part 3 explicitly asks for **Corner and Line deadlocks** (walls). Should we also support 2x2 box clumps (two boxes stuck together against a wall), or keep strictly to the wall-based deadlocks specified in Figures 5 and 6? (Recommended: stick to wall-based corner and line deadlocks as requested to avoid over-engineering).
