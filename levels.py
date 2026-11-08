from model import SokobanPuzzle

EXEMPLE_1_FIG7 = """
OOOOOOO
OS O RO
O  OB O
OS  B O
O  OB O
OS O  O
OOOOOOO
""".strip()

EXEMPLE_2_FIG7 = """
OOOOOOOO
OSSS OOO
O S B  O
O  BBB O
OOOO  RO
OOOOOOOO
""".strip()

LEVEL_1_FIG4 = """
OOOOOOOO
O      O
O R B SO
O      O
OOOOOOOO
""".strip()

LEVEL_2_FIG4 = """
OOOOOOOO
O     SO
O OOOOOO
O     RO
O BOOOOO
O      O
OOOOOOOO
""".strip()

LEVEL_3_FIG4 = """
OOOOOOOO
O  S   O
O  B   O
O  B   O
O  S   O
O  R   O
OOOOOOOO
""".strip()

LEVEL_4_FIG4 = """
OOOOOOOOOO
O   O    O
O B S  B O
O   O    O
O   O    O
O   OB S O
O R O    O
O   O    O
OOOOOOOOOO
""".strip()

LEVEL_5_FIG4 = """
OOOOOOOO
O      O
O B B  O
O  S   O
O  S   O
O  S B O
O   R  O
OOOOOOOO
""".strip()

ALL_LEVELS = [
    ("Figure 7 - Example 1 (3 boxes)", EXEMPLE_1_FIG7),
    ("Figure 7 - Example 2 (4 boxes)", EXEMPLE_2_FIG7),
    ("Figure 4 - Example 1 (1 box)", LEVEL_1_FIG4),
    ("Figure 4 - Example 2 (1 box)", LEVEL_2_FIG4),
    ("Figure 4 - Example 3 (2 boxes)", LEVEL_3_FIG4),
    ("Figure 4 - Example 4 (3 boxes)", LEVEL_4_FIG4),
    ("Figure 4 - Example 5 (3 boxes)", LEVEL_5_FIG4),
]

def get_level(index):
    name, layout = ALL_LEVELS[index - 1]
    return name, SokobanPuzzle(layout)
