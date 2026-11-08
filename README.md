# Sokoban Solver (Project 1 - Part 3): Deadlock Detection & Search Pruning

**USTHB — Master 1 Visual Computing (2026/2027)**  
**Module:** Problem Solving (Résolution de Problèmes)  
**Instructor:** Dr. Meriem SEBAI  
**Project:** Modeling and Solving the Sokoban Puzzle — Part 3 (Deadlocks & Search Improvement)

---

## 1. What's New in Part 3?

In Part 1 and Part 2, we formulated the game, built Breadth-First Search (BFS), implemented A* with heuristics ($h_1, h_2, h_3$), and visualized solutions on Figure 4 levels.

However, as puzzles scale up (more boxes, longer corridors, bottleneck doorways), standard search algorithms suffer from a catastrophic problem: **The Search Space Explosion of Doomed Subtrees**.

When a player pushes a box into an unrecoverable position (a **deadlock**), that state can **never** reach a goal. Yet, blind BFS and standard A* continue blindly exploring millions of descendant states—moving the player around, pushing other boxes—wasting enormous memory and CPU time exploring a branch that is mathematically doomed from the very first bad push.

**Part 3 introduces two major advancements:**
1. **Geometric Deadlock Detection:** Formal detection of **Corner Deadlocks** (Figure 5) and **Line Deadlocks** (Figure 6).
2. **Hard Search Pruning:** Modifying the A* search loop so that deadlocked successors are discarded **immediately** during move generation, preventing them from ever entering the search tree or consuming queue memory.

---

## 2. Deep Dive: The Theory of Deadlocks

A **deadlock** in Sokoban is a state from which no sequence of legal moves can ever reach the goal state. Because boxes can only be pushed and never pulled, a box trapped in a deadlock position is permanently ruined.

### 2.1 Corner Deadlocks (Figure 5)

A **Corner Deadlock** occurs when a box rests on a non-storage tile $(r, c) \notin S$ surrounded by two walls meeting at a 90-degree angle.

```
       WALL (O)                        WALL (O)
   WALL (O)  BOX (B)              BOX (B)  WALL (O)
       (North-West)                    (North-East)

   WALL (O)  BOX (B)              BOX (B)  WALL (O)
       WALL (O)                        WALL (O)
       (South-West)                    (South-East)
```

#### Why it is stuck:
* To push the box vertically (North or South), the player must stand directly on the opposite side. But that side is blocked by a solid wall!
* To push the box horizontally (West or East), the player must stand on the opposite side, which is also blocked by a solid wall!
* The box has **zero degrees of freedom**. It can never leave that tile. If that tile is not a storage target `'S'`, the game is permanently lost.

#### Mathematical Condition:
For any non-target floor tile $(r, c) \notin S$:
$$\text{IsCorner}(r, c) \iff (\text{Wall}_N \land \text{Wall}_W) \lor (\text{Wall}_N \land \text{Wall}_E) \lor (\text{Wall}_S \land \text{Wall}_W) \lor (\text{Wall}_S \land \text{Wall}_E)$$

---

### 2.2 Line Deadlocks (Figure 6)

A **Line Deadlock** is much more subtle and insidious than a corner deadlock. In Figure 6 of the project PDF, these are the tiles marked in **yellow**.

Consider a flat, straight wall. A crate pushed against this wall touches only **one** wall. It is not in a corner. Why is it a deadlock?

```
      WALL (O)   WALL (O)   WALL (O)   WALL (O)   WALL (O)
      CORNER        ·       BOX (B)       ·       CORNER
   [Deadlock]   (Yellow)    (Yellow)   (Yellow)   [Deadlock]
```

#### The Trap Mechanism:
1. Because the wall is completely solid on one side (e.g., North), the player can **never stand on the other side** to push the box downwards away from the wall.
2. The player can only push the box **parallel** to the wall (left or right).
3. If the box slides left, it eventually hits the left corner deadlock.
4. If the box slides right, it eventually hits the right corner deadlock.
5. If there are **no storage targets `'S'` anywhere along that entire wall segment**, the crate is permanently trapped on that wall forever!

#### Formal Line Deadlock Algorithm:
To detect line deadlocks statically:
1. Identify all Corner Deadlock tiles on the board.
2. For every pair of corner deadlocks $C_1 = (r_1, c_1)$ and $C_2 = (r_2, c_2)$:
   * **Horizontal Segment ($r_1 = r_2$):** Check all intermediate tiles $(r_1, c)$ for $c_1 < c < c_2$. If all intermediate tiles are floor spaces, none are storage targets, and the adjacent side (either all $r_1-1$ or all $r_1+1$) is an unbroken row of walls, then **every tile along that segment is a Line Deadlock**.
   * **Vertical Segment ($c_1 = c_2$):** Check all intermediate tiles $(r, c_1)$ for $r_1 < r < r_2$. If all intermediate tiles are floor spaces, none are storage targets, and the adjacent side (either all $c_1-1$ or all $c_1+1$) is an unbroken column of walls, then **every tile along that segment is a Line Deadlock**.

---

## 3. The Algorithmic Leap: Soft Penalty vs. Hard Pruning

In Part 2, we experimented with corner deadlocks by adding a $+1000$ penalty inside heuristic $h_3$. In Part 3, we replace this with **Hard Pruning inside the A* search loop**.

Here is why this distinction is revolutionary:

| Dimension | Part 2: Soft Penalty ($h_3$) | Part 3: Hard Pruning (Improved A*) |
| :--- | :--- | :--- |
| **Location** | Inside `heuristics.py` | Inside `search.py` (Successor loop) |
| **State Creation** | State is generated, wrapped into a `Node` | Deadlocked state is rejected on the spot |
| **Memory Allocation** | Yes (allocated in RAM and pushed to heap) | **Zero** (never enters the heap queue) |
| **Exploration Impact** | Node sits deep in the priority queue | **Pruned entirely** (subtree cut off at root) |
| **Computational Cost** | High (heap push/pop overhead, deep queue) | Extremely low ($O(1)$ set lookup) |

### Code Comparison

#### Part 2 (Soft Penalty):
```python
# heuristics.py
def h3(puzzle):
    if is_corner_deadlock(puzzle, r, c):
        return base_h2 + 1000  # Slaps a penalty, but Node still gets created!
```

#### Part 3 (Hard Pruning):
```python
# search.py: Improved_A_Star
for action, successor_state in current_node.state.successorFunction():
    if is_deadlock(successor_state, static_deadlocks):
        continue  # DROP IMMEDIATELY! Do not make Node, do not push to heap.
```

---

## 4. Code Architecture

```
project_3/
├── pyproject.toml        # Environment dependencies (Python 3.11, pygame 2.6.1)
├── .python-version       # Python runtime pin (3.11)
├── SPEC.md               # Formal specification approved before implementation
├── README.md             # This comprehensive master guide
├── model.py              # SokobanPuzzle & Node classes (comment-free)
├── deadlocks.py          # Static Corner & Line deadlock engine (comment-free)
├── heuristics.py         # Heuristic functions h1, h2, h3 (comment-free)
├── search.py             # BFS, Standard A*, and Improved A* with Hard Pruning
├── levels.py             # Figure 7 (Examples 1 & 2) and Figure 4 (Examples 1 to 5)
├── gui.py                # Pygame simulation studio adapted for Figure 7
├── test_deadlocks.py     # Unit test suite verifying Figures 5 & 6 deadlock sets
└── main.py               # Interactive CLI launcher with full comparison matrix
```

### Module Breakdown:

* **`deadlocks.py`:**
  * `get_corner_deadlocks(puzzle)`: Scans the grid for tiles with 2 perpendicular walls (Figure 5).
  * `get_line_deadlocks(puzzle, corners)`: Traces wall lines between corner deadlocks (Figure 6).
  * `get_static_deadlocks(puzzle)`: Precomputes the union of corner and line deadlocks once when a board is loaded.
  * `is_deadlock(puzzle, static_deadlocks)`: Returns `True` if any unplaced box sits on a precomputed dead tile in $O(1)$ time.

* **`search.py`:**
  * `BFS(initial_state)`: Baseline uninformed search.
  * `A_Star(initial_state, heuristic)`: Standard A* search without pruning.
  * `Improved_A_Star(initial_state, heuristic, static_deadlocks)`: The enhanced A* engine that enforces hard deadlock pruning before node generation.

* **`levels.py`:**
  * Pixel-perfect encodings of the two new test puzzles from **Figure 7**, plus the five puzzles from **Figure 4**.

---

## 5. Benchmark Results & Comparative Evaluation

All experiments were executed on Figure 7 puzzles using `uv run python main.py` (Option 4: Compare All Algorithms):

### 5.1 Figure 7 — Example 1 (3 Boxes, Bottleneck Wall)

```
OOOOOOO
OS O RO
O  OB O
OS  B O
O  OB O
OS O  O
OOOOOOO
```

| Algorithm | Optimal Cost ($g$) | Explored Nodes | Execution Time | Search Space Reduction |
| :--- | :---: | :---: | :---: | :---: |
| **BFS** | 41 | 2,307 | 0.049 s | Baseline |
| **Standard A* ($h_1$)** | 41 | 2,313 | 0.052 s | -0.2% |
| **Standard A* ($h_2$)** | 41 | 2,242 | 0.088 s | +2.8% |
| **Standard A* ($h_3$)** | 41 | 2,162 | 0.091 s | +6.3% |
| **Improved A* ($h_3$ + Deadlocks)** | **41** | **1,009** | **0.049 s** | **+53.3% reduction** |

---

### 5.2 Figure 7 — Example 2 (4 Boxes, Perimeter Walls & Corridors)

```
OOOOOOOO
OSSS OOO
O S B  O
O  BBB O
OOOO  RO
OOOOOOOO
```

| Algorithm | Optimal Cost ($g$) | Explored Nodes | Execution Time | Search Space Reduction |
| :--- | :---: | :---: | :---: | :---: |
| **BFS** | 55 | 54,726 | 1.412 s | Baseline |
| **Standard A* ($h_1$)** | 55 | 54,671 | 1.750 s | +0.1% |
| **Standard A* ($h_2$)** | 55 | 49,543 | 2.250 s | +9.5% |
| **Standard A* ($h_3$)** | 55 | 48,436 | 2.798 s | +11.5% |
| **Improved A* ($h_3$ + Deadlocks)** | **55** | **5,575** | **0.302 s** | **+88.5% reduction** |

---

### Key Scientific Observations:
1. **Admissibility Remains Uncompromised:** Across all algorithms, the optimal solution cost remains identical ($g = 41$ for Ex 1, $g = 55$ for Ex 2). Pruning deadlocks never discards a winning path because deadlocked states can never reach the goal.
2. **Massive Search Space Reduction on Complex Boards:** On Example 2, standard A* explored **48,436 nodes** before finding the solution. Improved A* found the exact same solution after exploring only **5,575 nodes**—slashing the state space by **88.5%** and speeding up execution by **9.2x**!
3. **The Bottleneck of Line Deadlocks:** Example 2 features long flat perimeter walls (rows 3 and 4). Without line deadlock detection, the solver wastes tens of thousands of expansions moving boxes up and down those doomed perimeter lines. Pruning cuts those branches off immediately.

---

## 6. Verification Suite

Run the unit tests to verify that the deadlock detection engine identifies the exact red dots (Figure 5) and yellow dots (Figure 6) from the project specification:

```bash
cd "/home/rma/Studies/M1/Problems Resolution/project_3"
uv run python -m unittest test_deadlocks.py
```

### Verified Assertions:
* **Example 1:**
  * Corners (Red): `{(1, 2), (1, 4), (1, 5), (5, 2), (5, 4), (5, 5)}`
  * Lines (Yellow): `{(2, 5), (3, 5), (4, 5)}`
* **Example 2:**
  * Corners (Red): `{(1, 4), (2, 6), (3, 1), (4, 4), (4, 6)}`
  * Lines (Yellow): `{(3, 6), (4, 5)}`
* Both tests pass with 100% compliance.

---

## 7. How to Run

### Requirements
* Python 3.11+
* `uv` package manager

### Launching the Interactive CLI:
```bash
cd "/home/rma/Studies/M1/Problems Resolution/project_3"
uv run python main.py
```

### Options:
1. Choose a level from the flat list (1–7):
   * `1` : Figure 7 - Example 1 (3 boxes)
   * `2` : Figure 7 - Example 2 (4 boxes)
   * `3-7` : Figure 4 - Examples 1 to 5
2. Choose Mode:
   * `1` : **Improved A*** ($h_3$ + Deadlock Pruning)
   * `2` : Standard A* ($h_1, h_2, h_3$)
   * `3` : BFS
   * `4` : **Compare All Algorithms** (prints side-by-side benchmark table)
3. Upon solving, press `[y]` to open the Pygame GUI simulation studio.
