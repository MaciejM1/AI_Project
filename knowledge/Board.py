from enum import Enum

import pygame
from constants import *
from images import *
import random
from knowledge.Home import *
from knowledge.RecyclingBin import *


class Board:
    # Konstruktor obiektu PLANSZA
    def __init__(self):

        # Lista pól - układ [kolumna] [wiersz]
        self.fields_list = []

        # Inicjalizacja listy dwuwymiarowej po ilości kolumn
        for i in range(COLS):
            self.fields_list.append(list())

        self.isWinter = False
        self.season = Season.SPRING

        # Listy obiektów na mapie

        # Domki
        self.home_list = []

        # Drzewa
        self.treePositions = [(1, 3), (2, 4), (5, 4), (8, 3), (8, 4), (9, 4), (14, 3), (11, 4), (16, 4),
                              (11, 5), (14, 5), (16, 5), (13, 6), (10, 7), (18, 0), (19, 0), (19, 1),
                              (19, 8), (19, 9), (18, 9), (6, 6), (7, 6), (7, 7), (7, 8), (8, 8), (8, 9), (9, 9), (5, 6)]

        # Zniszczone drogi
        self.roadPositions = [(0, 3), (1, 2), (5, 3), (11, 3), (12, 6), (8, 7), (15, 5), (7, 4), (1, 2)]

        # Błoto
        self.mudPositions = [(0, 2), (1, 4), (3, 4), (8, 6), (10, 3), (16, 3), (13, 5), (16, 6), (4, 3), (6, 4), (6, 5)]

        # Duże domki
        self.bigHomePositionsT = [(0, 0), (2, 0), (4, 0), (6, 0), (8, 0), (10, 0), (12, 0), (14, 0), (16, 0)]
        self.bigHomePositionsB = [(10, 9), (12, 9), (14, 9), (16, 9)]

        # Małe domki
        self.smallHomePositions = [(19, 2), (19, 3), (19, 4), (19, 5), (19, 6), (19, 7)]

        # Lista miejsc koszy
        self.bins_places_free = {(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1),
                                 (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1), (17, 1), (10, 8),
                                 (11, 8), (12, 8), (13, 8), (14, 8), (15, 8), (16, 8), (17, 8), (18, 2), (18, 3),
                                 (18, 4), (18, 5), (18, 6), (18, 7)}
        self.bins_places_taken = set()

        # Generowanie zbioru miejsc koszy
        for home in self.home_list:
            for bin_place in home.binsList:
                self.bins_places_free.add(bin_place)

    def generateBoard(self, screen):

        # Wypełnienie ekranu jednolitym kolorem
        screen.fill((0, 0, 0))
        for col in range(COLS):
            for row in range(ROWS):
                # Generowanie pól planszy o domyślnym typie TRAWA
                self.fields_list[col].append(Field(
                    pygame.draw.rect(screen, (0, 0, 0), (col * FIELD_SIZE, row * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE)),
                    row, col, FieldType.GRASS))

        # Definiowanie typu pól jako ZNISZCZONA DROGA
        for col, row in self.roadPositions:
            self.fields_list[col][row].fieldType = FieldType.BROKEN_ROAD

        # Definiowanie typu pól jako BŁOTO
        for col, row in self.mudPositions:
            self.fields_list[col][row].fieldType = FieldType.MUD

        # Definiowanie typu pól jako DOM, MIEJSCE NA KOSZ

        # Duże domki
        self.home_list.append(Home(1, HOME_BIG_1_RESIZED, HomeType.HOME_BIG, 0, 0, 0, 1, random.choice(IS_PAID)))
        self.fields_list[0][0].fieldObject = self.home_list[0]
        self.fields_list[1][0].fieldObject = self.home_list[0]
        self.fields_list[0][1].fieldObject = self.home_list[0].binsList[0]
        self.fields_list[1][1].fieldObject = self.home_list[0].binsList[1]
        self.home_list.append(Home(2, HOME_BIG_2_RESIZED, HomeType.HOME_BIG, 2, 0, 2, 1, random.choice(IS_PAID)))
        self.fields_list[2][0].fieldObject = self.home_list[1]
        self.fields_list[3][0].fieldObject = self.home_list[1]
        self.fields_list[2][1].fieldObject = self.home_list[1].binsList[0]
        self.fields_list[3][1].fieldObject = self.home_list[1].binsList[1]
        self.home_list.append(Home(3, HOME_BIG_3_RESIZED, HomeType.HOME_BIG, 4, 0, 4, 1, random.choice(IS_PAID)))
        self.fields_list[4][0].fieldObject = self.home_list[2]
        self.fields_list[5][0].fieldObject = self.home_list[2]
        self.fields_list[4][1].fieldObject = self.home_list[2].binsList[0]
        self.fields_list[5][1].fieldObject = self.home_list[2].binsList[1]
        self.home_list.append(Home(4, HOME_BIG_4_RESIZED, HomeType.HOME_BIG, 6, 0, 6, 1, random.choice(IS_PAID)))
        self.fields_list[6][0].fieldObject = self.home_list[3]
        self.fields_list[7][0].fieldObject = self.home_list[3]
        self.fields_list[6][1].fieldObject = self.home_list[3].binsList[0]
        self.fields_list[7][1].fieldObject = self.home_list[3].binsList[1]
        self.home_list.append(Home(5, HOME_BIG_5_RESIZED, HomeType.HOME_BIG, 8, 0, 8, 1, random.choice(IS_PAID)))
        self.fields_list[8][0].fieldObject = self.home_list[4]
        self.fields_list[9][0].fieldObject = self.home_list[4]
        self.fields_list[8][1].fieldObject = self.home_list[4].binsList[0]
        self.fields_list[9][1].fieldObject = self.home_list[4].binsList[1]
        self.home_list.append(Home(6, HOME_BIG_6_RESIZED, HomeType.HOME_BIG, 10, 0, 10, 1, random.choice(IS_PAID)))
        self.fields_list[10][0].fieldObject = self.home_list[5]
        self.fields_list[11][0].fieldObject = self.home_list[5]
        self.fields_list[10][1].fieldObject = self.home_list[5].binsList[0]
        self.fields_list[11][1].fieldObject = self.home_list[5].binsList[1]
        self.home_list.append(Home(7, HOME_BIG_7_RESIZED, HomeType.HOME_BIG, 12, 0, 12, 1, random.choice(IS_PAID)))
        self.fields_list[12][0].fieldObject = self.home_list[6]
        self.fields_list[13][0].fieldObject = self.home_list[6]
        self.fields_list[12][1].fieldObject = self.home_list[6].binsList[0]
        self.fields_list[13][1].fieldObject = self.home_list[6].binsList[1]
        self.home_list.append(Home(8, HOME_BIG_8_RESIZED, HomeType.HOME_BIG, 14, 0, 14, 1, random.choice(IS_PAID)))
        self.fields_list[14][0].fieldObject = self.home_list[7]
        self.fields_list[15][0].fieldObject = self.home_list[7]
        self.fields_list[14][1].fieldObject = self.home_list[7].binsList[0]
        self.fields_list[15][1].fieldObject = self.home_list[7].binsList[1]
        self.home_list.append(Home(9, HOME_BIG_9_RESIZED, HomeType.HOME_BIG, 16, 0, 16, 1, random.choice(IS_PAID)))
        self.fields_list[16][0].fieldObject = self.home_list[8]
        self.fields_list[17][0].fieldObject = self.home_list[8]
        self.fields_list[16][1].fieldObject = self.home_list[8].binsList[0]
        self.fields_list[17][1].fieldObject = self.home_list[8].binsList[1]
        self.home_list.append(Home(10, HOME_BIG_10_RESIZED, HomeType.HOME_BIG, 10, 9, 10, 8, random.choice(IS_PAID)))
        self.fields_list[10][9].fieldObject = self.home_list[9]
        self.fields_list[11][9].fieldObject = self.home_list[9]
        self.fields_list[10][8].fieldObject = self.home_list[9].binsList[0]
        self.fields_list[11][8].fieldObject = self.home_list[9].binsList[1]
        self.home_list.append(Home(11, HOME_BIG_11_RESIZED, HomeType.HOME_BIG, 12, 9, 12, 8, random.choice(IS_PAID)))
        self.fields_list[12][9].fieldObject = self.home_list[10]
        self.fields_list[13][9].fieldObject = self.home_list[10]
        self.fields_list[12][8].fieldObject = self.home_list[10].binsList[0]
        self.fields_list[13][8].fieldObject = self.home_list[10].binsList[1]
        self.home_list.append(Home(12, HOME_BIG_12_RESIZED, HomeType.HOME_BIG, 14, 9, 14, 8, random.choice(IS_PAID)))
        self.fields_list[14][9].fieldObject = self.home_list[11]
        self.fields_list[15][9].fieldObject = self.home_list[11]
        self.fields_list[14][8].fieldObject = self.home_list[11].binsList[0]
        self.fields_list[15][8].fieldObject = self.home_list[11].binsList[1]
        self.home_list.append(Home(13, HOME_BIG_13_RESIZED, HomeType.HOME_BIG, 16, 9, 16, 8, random.choice(IS_PAID)))
        self.fields_list[16][9].fieldObject = self.home_list[12]
        self.fields_list[17][9].fieldObject = self.home_list[12]
        self.fields_list[16][8].fieldObject = self.home_list[12].binsList[0]
        self.fields_list[17][8].fieldObject = self.home_list[12].binsList[1]

        # Małe domki
        self.home_list.append(Home(14, HOME_SMALL_1_RESIZED, HomeType.HOME_SMALL, 19, 2, 18, 2, random.choice(IS_PAID)))
        self.fields_list[19][2].fieldObject = self.home_list[13]
        self.fields_list[18][2].fieldObject = self.home_list[13].binsList[0]
        self.home_list.append(Home(15, HOME_SMALL_2_RESIZED, HomeType.HOME_SMALL, 19, 3, 18, 3, random.choice(IS_PAID)))
        self.fields_list[19][3].fieldObject = self.home_list[14]
        self.fields_list[18][3].fieldObject = self.home_list[14].binsList[0]
        self.home_list.append(Home(16, HOME_SMALL_3_RESIZED, HomeType.HOME_SMALL, 19, 4, 18, 4, random.choice(IS_PAID)))
        self.fields_list[19][4].fieldObject = self.home_list[15]
        self.fields_list[18][4].fieldObject = self.home_list[15].binsList[0]
        self.home_list.append(Home(17, HOME_SMALL_4_RESIZED, HomeType.HOME_SMALL, 19, 5, 18, 5, random.choice(IS_PAID)))
        self.fields_list[19][5].fieldObject = self.home_list[16]
        self.fields_list[18][5].fieldObject = self.home_list[16].binsList[0]
        self.home_list.append(Home(18, HOME_SMALL_5_RESIZED, HomeType.HOME_SMALL, 19, 6, 18, 6, random.choice(IS_PAID)))
        self.fields_list[19][6].fieldObject = self.home_list[17]
        self.fields_list[18][6].fieldObject = self.home_list[17].binsList[0]
        self.home_list.append(Home(19, HOME_SMALL_6_RESIZED, HomeType.HOME_SMALL, 19, 7, 18, 7, random.choice(IS_PAID)))
        self.fields_list[19][7].fieldObject = self.home_list[18]
        self.fields_list[18][7].fieldObject = self.home_list[18].binsList[0]

        for col, row in self.bigHomePositionsT:
            self.fields_list[col][row].fieldType = FieldType.HOME
            self.fields_list[col + 1][row].fieldType = FieldType.HOME
            self.fields_list[col][row + 1].fieldType = FieldType.BIN_PLACE
            self.fields_list[col + 1][row + 1].fieldType = FieldType.BIN_PLACE

        for col, row in self.bigHomePositionsB:
            self.fields_list[col][row].fieldType = FieldType.HOME
            self.fields_list[col + 1][row].fieldType = FieldType.HOME
            self.fields_list[col][row - 1].fieldType = FieldType.BIN_PLACE
            self.fields_list[col + 1][row - 1].fieldType = FieldType.BIN_PLACE

        for col, row in self.smallHomePositions:
            self.fields_list[col][row].fieldType = FieldType.HOME
            self.fields_list[col - 1][row].fieldType = FieldType.BIN_PLACE

        # Definiowanie pól jako WYSYPISKO, SEKTORY WYSYPISKA, STACJA TANKOWANIA

        # Wysypisko
        for i in range(0, 7):
            for j in range(7, 10):
                self.fields_list[i][j].blocked = True
                self.fields_list[i][j].fieldType = FieldType.GARBAGE_DUMP
        self.fields_list[8][9].blocked = True
        self.fields_list[8][9].fieldType = FieldType.GARBAGE_DUMP

        # Stacja tankowania
        self.fields_list[0][6].fieldType = FieldType.FUEL_STATION_SECTOR

        # Sektor - PLASTIK I METAL
        self.fields_list[1][6].fieldType = FieldType.PLASTIC_AND_METAL_SECTOR

        # Sektor - SZKŁO
        self.fields_list[2][6].fieldType = FieldType.GLASS_SECTOR

        # Sektor - PAPIER
        self.fields_list[3][6].fieldType = FieldType.PAPER_SECTOR

        # Sektor - BIOODPADY
        self.fields_list[4][6].fieldType = FieldType.BIO_SECTOR

    # Generowanie obiektów stałych - DRZEW, DOMKÓW, WYSYPISKA, PUNKTÓW WYRZUTU (SEKTORY), TANKOWANIA
    def drawConstantObjects(self, screen):

        # Wypełnienie ekranu jednolitym kolorem
        screen.fill((0, 0, 0))

        # Stworzenie planszy i wypełnienie ekranu - tekstura trawy
        for col in range(COLS):
            for row in range(ROWS):
                screen.blit(GRASS_RESIZED, self.fields_list[col][row].fieldRect)

        # Generowanie domków na ekranie
        for home in self.home_list:
            if home.homeType == HomeType.HOME_SMALL:
                screen.blit(home.homeImage,
                            home.homeImage.get_rect(
                                center=self.fields_list[home.startCol][home.startRow].fieldRect.center))
                self.fields_list[home.startCol][home.startRow].blocked = True
            else:
                screen.blit(home.homeImage, self.fields_list[home.startCol][home.startRow].fieldRect)
                self.fields_list[home.startCol][home.startRow].blocked = True
                self.fields_list[home.startCol + 1][home.startRow].blocked = True

        # Generowanie wysypiska i punktów wyrzucania [sektory]
        screen.blit(GARBAGE_DUMP_HILL_RESIZED, self.fields_list[0][7].fieldRect)
        screen.blit(FUEL_STATION_RESIZED, FUEL_STATION_RESIZED.get_rect(center=self.fields_list[0][6].fieldRect.center))
        screen.blit(RECYCLE_YELLOW_RESIZED,
                    RECYCLE_YELLOW_RESIZED.get_rect(center=self.fields_list[1][6].fieldRect.center))
        screen.blit(RECYCLE_GREEN_RESIZED,
                    RECYCLE_GREEN_RESIZED.get_rect(center=self.fields_list[2][6].fieldRect.center))
        screen.blit(RECYCLE_BLUE_RESIZED, RECYCLE_BLUE_RESIZED.get_rect(center=self.fields_list[3][6].fieldRect.center))
        screen.blit(RECYCLE_BROWN_RESIZED,
                    RECYCLE_BROWN_RESIZED.get_rect(center=self.fields_list[4][6].fieldRect.center))

        # Generowanie drzew
        for col, row in self.treePositions:
            self.drawObject(TREE_RESIZED, col, row, screen)

        # Generowanie zniszczonej drogi
        for col, row in self.roadPositions:
            screen.blit(BROKEN_ROAD_RESIZED,
                        BROKEN_ROAD_RESIZED.get_rect(center=self.fields_list[col][row].fieldRect.center))

        # Generowanie błota
        for col, row in self.mudPositions:
            screen.blit(MUD_RESIZED, MUD_RESIZED.get_rect(center=self.fields_list[col][row].fieldRect.center))

    def binSpawner(self, GTA):
        if len(self.bins_places_free) != 0:
            bin_place = random.sample(self.bins_places_free, 1)
            col = bin_place[0][0]
            row = bin_place[0][1]
            if (GTA.col != col or GTA.row != row):
                self.fields_list[col][row].fieldObject.binObject = RecyclingBin(random.choice(BIN_TYPES),
                                                                                random.randint(1, MAX_BIN_CAPACITY),
                                                                                random.choice(BIN_QUALITY),
                                                                                random.choice(BIN_BAG))
                print("[BIN_SPAWNER]: Wygenerowano kosz => [NrDomu: {}, Koordynaty: ({}, {}), Zajętość: {}/{}]".format(
                    self.fields_list[col][row].fieldObject.home, self.fields_list[col][row].fieldObject.col,
                    self.fields_list[col][row].fieldObject.row,
                    self.fields_list[col][row].fieldObject.binObject.amountOfWaste, MAX_BIN_CAPACITY))
                self.bins_places_free.remove((col, row))
                self.bins_places_taken.add((col, row))

                #print(self.bins_places_free)
                #print(self.bins_places_taken)
            else:
                if len(self.bins_places_free) > 1:
                    self.binSpawner(GTA)

    def addRubbish(self):
        if len(self.bins_places_taken) != 0:
            bin_place = random.sample(self.bins_places_taken, 1)
            col = bin_place[0][0]
            row = bin_place[0][1]
            level = self.fields_list[col][row].fieldObject.binObject.amountOfWaste
            if level != MAX_BIN_CAPACITY:
                self.fields_list[col][row].fieldObject.binObject.amountOfWaste += random.randint(5, 15)
                if self.fields_list[col][row].fieldObject.binObject.amountOfWaste > MAX_BIN_CAPACITY:
                    self.fields_list[col][row].fieldObject.binObject.amountOfWaste = MAX_BIN_CAPACITY
                print(
                    "[ADD_RUBBISH]: W koszu pojawiły się kolejne odpadki => [NrDomu: {}, Koordynaty: ({}, {}), Zajętość przed: {}/{}, Zajętość po: {}/{}]".format(
                        self.fields_list[col][row].fieldObject.home, self.fields_list[col][row].fieldObject.col,
                        self.fields_list[col][row].fieldObject.row, level, MAX_BIN_CAPACITY,
                        self.fields_list[col][row].fieldObject.binObject.amountOfWaste, MAX_BIN_CAPACITY))

    def randomizeRubbishParams(self, param):
        if len(self.bins_places_taken) != 0:
            bin_place = random.sample(self.bins_places_taken, 1)
            col = bin_place[0][0]
            row = bin_place[0][1]
            if param == 1:
                self.fields_list[col][row].fieldObject.binObject.isQuality = random.choice(BIN_QUALITY)
            elif param == 2:
                self.fields_list[col][row].fieldObject.binObject.isBag = random.choice(BIN_BAG)

    def randomizeHome(self):
        self.home_list[random.randint(0, len(self.home_list))-1].isPaid = random.choice(IS_PAID)

    def updateTime(self, time):
        for bin_place in self.bins_places_taken:
            col = bin_place[0]
            row = bin_place[1]
            self.fields_list[col][row].fieldObject.binObject.time += time

    # Generowanie pozostałych obiektów - ZMIENNYCH
    def drawTemporaryObjects(self, screen):

        # Generowanie koszy na ekranie
        for home in self.home_list:
            for binPlace in home.binsList:
                if binPlace.binObject != BinPlaceStatus.EMPTY:
                    screen.blit(binPlace.binObject.binImage, binPlace.binObject.binImage.get_rect(
                        center=self.fields_list[binPlace.col][binPlace.row].fieldRect.center))

    # Funkcja to rysowania obiektów na planszy
    def drawObject(self, objectImage, col, row, screen):
        screen.blit(objectImage, objectImage.get_rect(center=self.fields_list[col][row].fieldRect.center))
        self.fields_list[col][row].blocked = True


# Klasa - POLE - dla planszy
class Field:
    def __init__(self, fieldRect, col, row, type):
        self.fieldRect = fieldRect
        self.fieldType = type
        self.fieldObject = None
        self.col = col
        self.row = row
        self.blocked = False


# Klasa - TYP POLA - dla planszy
class FieldType(Enum):
    GRASS = 1,  # TRAWA
    BROKEN_ROAD = 2,  # ZNISZCZONA DROGA
    MUD = 3,  # BŁOTO
    HOME = 4,  # DOM
    GARBAGE_DUMP = 5,  # WYSYPISKO
    BIN_PLACE = 6,  # MIEJSCE NA KOSZ
    PLASTIC_AND_METAL_SECTOR = 7,  # SEKTOR PLASTIKU I METALU
    GLASS_SECTOR = 8,  # SEKTOR SZKŁA
    PAPER_SECTOR = 9,  # SEKTOR PAPIERU
    BIO_SECTOR = 10,  # SEKTOR BIOODPADÓW
    FUEL_STATION_SECTOR = 11  # STACJA TANKOWANIA

class Season(Enum):
    SPRING = 1,
    SUMMER = 2,
    AUTUMN = 3,
    WINTER = 4

