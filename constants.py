import pygame

# Klatki na sekunde
FPS = 120

# Wymiary okna
WIDTH = 1440 / 1.5
HEIGHT = 720 / 1.5

# Liczba kolumn/wierszy
COLS, ROWS = 20, 10

# Długość boku jednego pola planszy
FIELD_SIZE = WIDTH // COLS

# Koszty typów pól
GRASS_COST = 1
BROKEN_ROAD_COST = 5
MUD_COST = 10

# Zakresy numeracji plików z zawartością kosza [1 - MAX]
MAX_PAPER = 835
MAX_GLASS = 1593
MAX_PLASTIC = 2559
MAX_BIO = 754

# Pojemność śmietnika
MAX_BIN_CAPACITY = 50

# Pojemność komory śmieciarki
MAX_CHAMBER_CAPACITY = 600

# Pojemność zbiorniku paliwa
MAX_FUEL_TANK_CAPACITY = 1000

# Zakres losowości między kolejnymi pojawieniami się śmietników
NEXT_BIN_MIN = 500
NEXT_BIN_MAX = 2500

# Inne
NEXT_PHASE_TIME = 30000
LONG_TIME = NEXT_PHASE_TIME/2

