import time
from levels import ALL_LEVELS, get_level
from heuristics import h1, h2, h3
from search import BFS, A_Star, Improved_A_Star
from gui import render_gui

def main():
    print("=" * 60)
    print("  SOKOBAN SOLVER & DEADLOCK ENGINE (PROJECT 1 - PART 3)")
    print("  USTHB - M1 Visual Computing (Problem Solving)")
    print("=" * 60)

    while True:
        print("\nSelect a level to solve (or 'q' to quit):")
        for i, (name, _) in enumerate(ALL_LEVELS, 1):
            print(f"  {i}) {name}")

        choice = input(f"\nChoose level (1-{len(ALL_LEVELS)}) or q: ").strip().lower()
        if choice == 'q':
            print("Exiting.")
            break

        if not (choice.isdigit() and 1 <= int(choice) <= len(ALL_LEVELS)):
            print("Invalid selection. Try again.")
            continue

        level_idx = int(choice)
        level_name, puzzle = get_level(level_idx)
        print(f"\n[+] Loaded: {level_name}")

        print("\nSelect Mode:")
        print("  1) Improved A* (Deadlock Pruning + h3) [Recommended]")
        print("  2) Standard A*")
        print("  3) BFS (Breadth-First Search)")
        print("  4) Compare All Algorithms (Benchmark Matrix)")

        mode = input("Choose mode (1-4) [default: 1]: ").strip()
        if mode == "":
            mode = "1"

        if mode == "4":
            print(f"\nRunning benchmark matrix on: {level_name}...")
            print("-" * 65)
            print(f"{'Algorithm':<28} | {'Cost':<6} | {'Explored':<10} | {'Time (s)':<8}")
            print("-" * 65)

            matrix = [
                ("BFS", lambda p: BFS(p)),
                ("A* (h1: unplaced)", lambda p: A_Star(p, h1)),
                ("A* (h2: Manhattan)", lambda p: A_Star(p, h2)),
                ("A* (h3: proximity)", lambda p: A_Star(p, h3)),
                ("Improved A* (h3 + Deadlocks)", lambda p: Improved_A_Star(p, h3)),
            ]

            best_solution = None
            best_explored = 0

            for algo_label, algo_fn in matrix:
                t0 = time.perf_counter()
                sol, exp = algo_fn(puzzle)
                elapsed = time.perf_counter() - t0

                if "Improved" in algo_label and sol is not None:
                    best_solution = sol
                    best_explored = exp

                cost_str = str(sol.g) if sol else "FAIL"
                print(f"{algo_label:<28} | {cost_str:<6} | {exp:<10} | {elapsed:.3f} s")

            print("-" * 65)

            if best_solution:
                launch_gui = input("\nLaunch Pygame visualization with Improved A* solution? (y/n) [y]: ").strip().lower()
                if launch_gui in ("", "y", "yes"):
                    render_gui(puzzle, best_solution, best_explored, algo_name="Improved A* (h3 + Deadlocks)")
            continue

        if mode == "1":
            print("\nAlgorithm: Improved A* (h3 with Corner & Line Deadlock Pruning)")
            t0 = time.perf_counter()
            sol, exp = Improved_A_Star(puzzle, h3)
            elapsed = time.perf_counter() - t0
            algo_title = "Improved A* (h3 + Deadlocks)"

        elif mode == "2":
            print("\nSelect Heuristic for Standard A*:")
            print("  1) h1 (Unplaced boxes)")
            print("  2) h2 (Manhattan distance sum)")
            print("  3) h3 (Robot proximity)")
            h_choice = input("Select heuristic (1-3) [default: 3]: ").strip()
            if h_choice == "1":
                h_fn = h1
                h_lbl = "h1"
            elif h_choice == "2":
                h_fn = h2
                h_lbl = "h2"
            else:
                h_fn = h3
                h_lbl = "h3"

            print(f"\nAlgorithm: Standard A* ({h_lbl})")
            t0 = time.perf_counter()
            sol, exp = A_Star(puzzle, h_fn)
            elapsed = time.perf_counter() - t0
            algo_title = f"Standard A* ({h_lbl})"

        elif mode == "3":
            print("\nAlgorithm: Breadth-First Search (BFS)")
            t0 = time.perf_counter()
            sol, exp = BFS(puzzle)
            elapsed = time.perf_counter() - t0
            algo_title = "BFS"

        else:
            print("Invalid mode. Returning to level selection.")
            continue

        if sol:
            actions = sol.getSolution()
            print(f"\n[+] Solution Found!")
            print(f"Moves: {actions}")
            print(f"Cost: {sol.g}")
            print(f"Explored Nodes: {exp}")
            print(f"Time: {elapsed:.3f} s")

            launch_gui = input("\nLaunch GUI visualizer? (y/n) [y]: ").strip().lower()
            if launch_gui in ("", "y", "yes"):
                render_gui(puzzle, sol, exp, algo_name=algo_title)
        else:
            print("\n[-] No solution found.")

if __name__ == '__main__':
    main()
