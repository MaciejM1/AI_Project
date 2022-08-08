import pygame
from images import *
from constants import MAX_PLASTIC, MAX_PAPER, MAX_GLASS, MAX_BIO, MAX_BIN_CAPACITY
import random


# Klasa kosz na śmieci
class RecyclingBin:
    def __init__(self, binType, amountOfWaste, isQuality, isBag):
        # Typ pojemnika
        # 1 - pojemnik na tworzywa sztuczne i metale
        # 2 - pojemnik na szkło
        # 3 - pojemnik na papier
        # 4 - pojemnik na bioodpady
        # 5 - pojemnik na  odpady zmieszane
        self.binType = binType
        # Ikona/kolor [definiowany przez typ]
        self.binImage = None
        # Fotografia zawartości kosza - SIECI NEURONOWE
        self.contentImage = None
        if binType == BinType.PLASTIC_AND_METAL:
            self.binImage = BIN_YELLOW_RESIZED
            path = "\\neuralNet\\contentImages\\plastic\\plastic" + str(random.randint(1, MAX_PLASTIC)) + ".jpg"
            self.contentImage = path
        if binType == BinType.GLASS:
            self.binImage = BIN_GREEN_RESIZED
            path = "\\neuralNet\\contentImages\\glass\\glass" + str(random.randint(1, MAX_GLASS)) + ".jpg"
            self.contentImage = path
        if binType == BinType.PAPER:
            self.binImage = BIN_BLUE_RESIZED
            path = "\\neuralNet\\contentImages\\paper\\paper" + str(random.randint(1, MAX_PAPER)) + ".jpg"
            self.contentImage = path
        if binType == BinType.BIO:
            self.binImage = BIN_BROWN_RESIZED
            path = "\\neuralNet\\contentImages\\bio\\bio" + str(random.randint(1, MAX_BIO)) + ".jpg"
            self.contentImage = path
        # Czas stania kosza
        self.time = 0
        # Czy kosz spełnia standardy jakości (np. ma specjalny uchwyt)
        self.isQuality = isQuality
        # Czy śmieci w koszu są w specjalnym śmietniku (wymogi jakościowe śmieciarki)
        self.isBag = isBag
        # Pojemność (maksymalna)
        self.capacity = MAX_BIN_CAPACITY
        # Ilość odpadów w pojemniku (0-MAX)
        self.amountOfWaste = amountOfWaste


# Klasa typ kosza na śmieci
class BinType(enumerate):
    PLASTIC_AND_METAL = 1,
    GLASS = 2,
    PAPER = 3,
    BIO = 4

# Lista typów koszy
BIN_TYPES = [BinType.PLASTIC_AND_METAL, BinType.GLASS, BinType.PAPER, BinType.BIO]
BIN_QUALITY = [False, True, True, True, False, True, True, True]
BIN_BAG = [True, True, True, False, True, True, True, False]
