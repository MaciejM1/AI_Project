import pygame
from constants import FIELD_SIZE

# Ikona gry/programu
GAME_ICON = pygame.image.load('images/GarbageTruckIcon.png')

# Wysypisko
GARBAGE_DUMP_HILL = pygame.image.load('images/GarbageDump.png')
GARBAGE_DUMP_HILL_RESIZED = pygame.transform.scale(GARBAGE_DUMP_HILL, (FIELD_SIZE * 8, FIELD_SIZE * 3))
# Oznakowanie wyrzutu tworzyw sztucznych i metali [SEKTOR 1]
RECYCLE_YELLOW = pygame.image.load('images/RECYCLE_YELLOW.png')
RECYCLE_YELLOW_RESIZED = pygame.transform.scale(RECYCLE_YELLOW, (FIELD_SIZE - 15, FIELD_SIZE - 15))
# Oznakowanie wyrzutu szkła [SEKTOR 2]
RECYCLE_GREEN = pygame.image.load('images/RECYCLE_GREEN.png')
RECYCLE_GREEN_RESIZED = pygame.transform.scale(RECYCLE_GREEN, (FIELD_SIZE - 15, FIELD_SIZE - 15))
# Oznakowanie wyrzutu papieru [SEKTOR 3]
RECYCLE_BLUE = pygame.image.load('images/RECYCLE_BLUE.png')
RECYCLE_BLUE_RESIZED = pygame.transform.scale(RECYCLE_BLUE, (FIELD_SIZE - 15, FIELD_SIZE - 15))
# Oznakowanie wyrzutu bioodpadów [SEKTOR 4]
RECYCLE_BROWN = pygame.image.load('images/RECYCLE_BROWN.png')
RECYCLE_BROWN_RESIZED = pygame.transform.scale(RECYCLE_BROWN, (FIELD_SIZE - 15, FIELD_SIZE - 15))
# Oznakowanie wyrzutu odpadów zmieszanych [SEKTOR 5]
RECYCLE_BLACK = pygame.image.load('images/RECYCLE_BLACK.png')
RECYCLE_BLACK_RESIZED = pygame.transform.scale(RECYCLE_BLACK, (FIELD_SIZE - 15, FIELD_SIZE - 15))
# Dystrybutor paliwa
FUEL_STATION = pygame.image.load('images/FUEL_STATION.png')
FUEL_STATION_RESIZED = pygame.transform.scale(FUEL_STATION, (FIELD_SIZE - 10, FIELD_SIZE - 10))

# Kosze na śmieci
# Tworzywa sztuczne i metale
BIN_YELLOW = pygame.image.load('images/BIN_YELLOW.png')
BIN_YELLOW_RESIZED = pygame.transform.scale(BIN_YELLOW, (FIELD_SIZE - 15, FIELD_SIZE - 5))
# Szkło
BIN_GREEN = pygame.image.load('images/BIN_GREEN.png')
BIN_GREEN_RESIZED = pygame.transform.scale(BIN_GREEN, (FIELD_SIZE - 15, FIELD_SIZE - 5))
# Papier
BIN_BLUE = pygame.image.load('images/BIN_BLUE.png')
BIN_BLUE_RESIZED = pygame.transform.scale(BIN_BLUE, (FIELD_SIZE - 15, FIELD_SIZE - 5))
# Bioodpady
BIN_BROWN = pygame.image.load('images/BIN_BROWN.png')
BIN_BROWN_RESIZED = pygame.transform.scale(BIN_BROWN, (FIELD_SIZE - 15, FIELD_SIZE - 5))
# Odpady zmieszane
BIN_BLACK = pygame.image.load('images/BIN_BLACK.png')
BIN_BLACK_RESIZED = pygame.transform.scale(BIN_BLACK, (FIELD_SIZE - 15, FIELD_SIZE - 5))

# Śmieciarka
GARBAGE_TRUCK = pygame.image.load('images/GARBAGE_TRUCK.PNG')
GARBAGE_TRUCK_RESIZED_RIGHT = pygame.transform.scale(GARBAGE_TRUCK, (FIELD_SIZE, FIELD_SIZE))
GARBAGE_TRUCK_RESIZED_LEFT = pygame.transform.flip(GARBAGE_TRUCK_RESIZED_RIGHT, True, False)
GARBAGE_TRUCK_RESIZED_UP = pygame.transform.rotate(GARBAGE_TRUCK_RESIZED_RIGHT, 90)
GARBAGE_TRUCK_RESIZED_DOWN = pygame.transform.rotate(GARBAGE_TRUCK_RESIZED_RIGHT, -90)

# Trawa
GRASS = pygame.image.load('images/Grass.png')
GRASS_RESIZED = pygame.transform.scale(GRASS, (FIELD_SIZE, FIELD_SIZE))
# Drzewo
TREE = pygame.image.load('images/Tree.png')
TREE_RESIZED = pygame.transform.scale(TREE, (FIELD_SIZE, FIELD_SIZE))
# Błoto
MUD = pygame.image.load('images/MUD.png')
MUD_RESIZED = pygame.transform.scale(MUD, (FIELD_SIZE, FIELD_SIZE))
# Zniszczona droga
BROKEN_ROAD = pygame.image.load('images/BROKEN_ROAD.png')
BROKEN_ROAD_RESIZED = pygame.transform.scale(BROKEN_ROAD, (FIELD_SIZE, FIELD_SIZE))

# Domki duże [dwa miejsza na kosze/odpadki]
HOME_BIG_1 = pygame.image.load('images/HOME_BIG_1.png')
HOME_BIG_1_RESIZED = pygame.transform.scale(HOME_BIG_1, (FIELD_SIZE * 2, FIELD_SIZE))
HOME_BIG_2 = pygame.image.load('images/HOME_BIG_2.png')
HOME_BIG_2_RESIZED = pygame.transform.scale(HOME_BIG_2, (FIELD_SIZE * 2, FIELD_SIZE))
HOME_BIG_3 = pygame.image.load('images/HOME_BIG_3.png')
HOME_BIG_3_RESIZED = pygame.transform.scale(HOME_BIG_3, (FIELD_SIZE * 2, FIELD_SIZE))
HOME_BIG_4 = pygame.image.load('images/HOME_BIG_4.png')
HOME_BIG_4_RESIZED = pygame.transform.scale(HOME_BIG_4, (FIELD_SIZE * 2, FIELD_SIZE))
HOME_BIG_5 = pygame.image.load('images/HOME_BIG_5.png')
HOME_BIG_5_RESIZED = pygame.transform.scale(HOME_BIG_5, (FIELD_SIZE * 2, FIELD_SIZE))
HOME_BIG_6 = pygame.image.load('images/HOME_BIG_6.png')
HOME_BIG_6_RESIZED = pygame.transform.scale(HOME_BIG_6, (FIELD_SIZE * 2, FIELD_SIZE))
HOME_BIG_7 = pygame.image.load('images/HOME_BIG_7.png')
HOME_BIG_7_RESIZED = pygame.transform.scale(HOME_BIG_7, (FIELD_SIZE * 2, FIELD_SIZE))
HOME_BIG_8 = pygame.image.load('images/HOME_BIG_8.png')
HOME_BIG_8_RESIZED = pygame.transform.scale(HOME_BIG_8, (FIELD_SIZE * 2, FIELD_SIZE))
HOME_BIG_9 = pygame.image.load('images/HOME_BIG_9.png')
HOME_BIG_9_RESIZED = pygame.transform.scale(HOME_BIG_9, (FIELD_SIZE * 2, FIELD_SIZE))
HOME_BIG_10 = pygame.image.load('images/HOME_BIG_10.png')
HOME_BIG_10_RESIZED = pygame.transform.scale(HOME_BIG_10, (FIELD_SIZE * 2, FIELD_SIZE))
HOME_BIG_11 = pygame.image.load('images/HOME_BIG_11.png')
HOME_BIG_11_RESIZED = pygame.transform.scale(HOME_BIG_11, (FIELD_SIZE * 2, FIELD_SIZE))
HOME_BIG_12 = pygame.image.load('images/HOME_BIG_12.png')
HOME_BIG_12_RESIZED = pygame.transform.scale(HOME_BIG_12, (FIELD_SIZE * 2, FIELD_SIZE))
HOME_BIG_13 = pygame.image.load('images/HOME_BIG_13.png')
HOME_BIG_13_RESIZED = pygame.transform.scale(HOME_BIG_13, (FIELD_SIZE * 2, FIELD_SIZE))

# Domki małe [jedna kratka, jedno miejsce na kosz/odpadki]
HOME_SMALL_1 = pygame.image.load('images/HOME_SMALL_1.png')
HOME_SMALL_1_RESIZED = pygame.transform.scale(HOME_SMALL_1, (FIELD_SIZE - 5, FIELD_SIZE - 5))
HOME_SMALL_2 = pygame.image.load('images/HOME_SMALL_2.png')
HOME_SMALL_2_RESIZED = pygame.transform.scale(HOME_SMALL_2, (FIELD_SIZE - 5, FIELD_SIZE - 5))
HOME_SMALL_3 = pygame.image.load('images/HOME_SMALL_3.png')
HOME_SMALL_3_RESIZED = pygame.transform.scale(HOME_SMALL_3, (FIELD_SIZE - 5, FIELD_SIZE - 5))
HOME_SMALL_4 = pygame.image.load('images/HOME_SMALL_4.png')
HOME_SMALL_4_RESIZED = pygame.transform.scale(HOME_SMALL_4, (FIELD_SIZE - 5, FIELD_SIZE - 5))
HOME_SMALL_5 = pygame.image.load('images/HOME_SMALL_5.png')
HOME_SMALL_5_RESIZED = pygame.transform.scale(HOME_SMALL_5, (FIELD_SIZE - 5, FIELD_SIZE - 5))
HOME_SMALL_6 = pygame.image.load('images/HOME_SMALL_6.png')
HOME_SMALL_6_RESIZED = pygame.transform.scale(HOME_SMALL_6, (FIELD_SIZE - 5, FIELD_SIZE - 5))
