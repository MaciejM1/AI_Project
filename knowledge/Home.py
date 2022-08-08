import pygame

from constants import *
from images import *


# Klasa domu
class Home:
    # Konstruktor obiektu DOM
    def __init__(self, homeNumber, homeImage, homeType, startCol, startRow, binCol, binRow, isPaid):
        # Numer domu
        self.homeNumber = homeNumber
        # Ikona domu
        self.homeImage = homeImage
        # Typ domu
        # [mały - jedno miejsce na kosz/odpadki (WARTOŚĆ 1, WYMIARY 1x1)]
        # [duży - dwa miejsca na kosz/odpadki (WARTOŚĆ 2, WYMIARY 2x1]
        self.homeType = homeType
        # Numer kolumny [jeżeli typ = duży - kolumny startowej] (numery 0-19)
        self.startCol = startCol
        # Numer wiersza (numery 0-9)
        self.startRow = startRow
        # Lista koszy
        self.binsList = list()
        self.binsList.append(BinPlace(self.homeNumber, BinPlaceStatus.EMPTY, binCol, binRow))
        if self.homeType == HomeType.HOME_BIG:
            self.binsList.append(BinPlace(self.homeNumber, BinPlaceStatus.EMPTY, binCol + 1, binRow))
        # Czy wywóz śmieci został opłacony
        self.isPaid = isPaid


# Klasa typu domu
class HomeType(enumerate):
    HOME_SMALL = 1,
    HOME_BIG = 2


# Klasa miejsce kosza
class BinPlace:
    def __init__(self, homeNumber, binObject, col, row):
        # Numer domu przy którym znajduje się miejsce
        self.home = homeNumber
        # Numer kolumny
        self.col = col
        # Numer wiersza
        self.row = row
        # Obiekt kosz [Może być puste miejsce - None]
        self.binObject = binObject

class BinPlaceStatus(enumerate):
    EMPTY = None

IS_PAID = [False, True, True, False, True, True, True, True, True, True]
