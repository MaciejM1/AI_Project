import pygame
from constants import *
from images import *

# Klasa sektora wysypiska
class Sector:
    def __init__(self, sectorType, col, row, icon):
        # Typ sektora
        # 1 - sektor tworzyw sztucznych i metali
        # 2 - sektor szkła
        # 3 - sektor papieru
        # 4 - sektor bioodpadów
        # 5 - sektor odpadów zmieszanych
        self.sectorType = sectorType
        # Liczba ilości odpadów [na start 0]
        self.amountOfWaste = 0
        # Numer kolumny miejsca wyrzutu odpadów
        self.col = col
        # Numer wiersza miejsca wyrzutu odpadów
        self.row = row
        # Ikona miejsca wyrzutu odpadów
        self.icon = icon

# Klasa typu sektora
class SectorType(enumerate):
    PLASTIC_AND_METAL = 1,
    GLASS = 2,
    PAPER = 3,
    BIO = 4,
    MIXED = 5
