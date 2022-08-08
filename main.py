import os

import pygame
import torch
import torch.nn as nn
from torchvision.transforms import transforms
from torch.utils.data import DataLoader
import numpy as np
from torch.autograd import Variable
from torchvision.models import squeezenet1_1
import torch.functional as F
from io import open
from PIL import Image
import torch.optim
import glob
import pandas as pd
from sklearn.tree import export_graphviz, export_text
from sklearn.tree import DecisionTreeClassifier
import random

from knowledge.Board import Board, Season
from knowledge.GarbageTruckAgent import GarbageTruckAgent
from knowledge.GarbageDump import *
from knowledge.Sector import *
from knowledge.PathGenerator import *
from neuralNet import neuralModel
from decisionTree import decisionTree
from geneticAlgorithm import geneticAlgorithm

# Inicjalizacja biblioteki pygame
pygame.init()

# Tworzenie ekranu gry (okienka)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Ustawienie nazwy/tytułu gry (okienka)
pygame.display.set_caption("Garbage Truck Agent AI")

# Ustawienie ikony gry (okienka)
pygame.display.set_icon(GAME_ICON)

# Pozycja startowa
start_col = 0
start_row = 5

# Stworzenie obiektu planszy
BOARD = Board()

# Generowanie planszy (pól)
BOARD.generateBoard(SCREEN)
BOARD.drawConstantObjects(SCREEN)
BOARD.drawTemporaryObjects(SCREEN)

# Stworzenie obiektu wysypiska i sektorów
GARBAGE_DUMP = GarbageDump(GARBAGE_DUMP_HILL_RESIZED, 0, 7)

# Stworzenie agenta
GTA = GarbageTruckAgent(
    GARBAGE_TRUCK_RESIZED_RIGHT.get_rect(center=BOARD.fields_list[start_col][start_row].fieldRect.center), start_col,
    start_row, GARBAGE_TRUCK_RESIZED_UP)

# Sieci neuronowe - klasyfikacja odpadów

device = neuralModel.device
transformer = neuralModel.transformer
classes = neuralModel.classes
model = neuralModel.model
optimizer = neuralModel.optimizer 
lossFunction = neuralModel.lossFunction
checkpoint = neuralModel.checkpoint
model.load_state_dict(checkpoint)
model.eval()

# Lista kolejnych ruchów z algorytmu A* z uwzględnionymi kosztami
moves = []

# Warunek startowy działania programu
run = True

# Zegar służący do ograniczenia ilości klatek na sekundę
clock = pygame.time.Clock()
last_action = 0
i = 1
currTime = 0
chapter = 1
print("[SEASON]: Obecna pora roku to => {}.".format(BOARD.season.name))
# Losowy czas generowania następnego kosza
nextBinTime = random.randint(NEXT_BIN_MIN, NEXT_BIN_MAX)
# Główna pętla działania programu/gry
while run:
    # print(BOARD.fields_list[0][1].fieldType.name)
    # print(BOARD.fields_list[4][6].fieldType)

    # Ustawienie zegara na [FPS - stała] klatek na sekundę
    dt = clock.tick(FPS)
    currTime += dt
    last_action += dt

    if last_action > nextBinTime and currTime < 20000 and chapter == 1:
        BOARD.binSpawner(GTA)
        BOARD.addRubbish()
        BOARD.updateTime(last_action)
        BOARD.randomizeHome()
        BOARD.randomizeRubbishParams(1)
        BOARD.randomizeRubbishParams(2)
        last_action = 0
        nextBinTime = random.randint(NEXT_BIN_MIN, NEXT_BIN_MAX)

    if currTime >= 20000 and chapter != 2:
        print("[AGENT_START]: Agent wyrusza do pracy!")
        moves = GTA.setupRoute(geneticAlgorithm.geneticAlgorithmPlot(population=list(BOARD.bins_places_taken), popSize=100, eliteSize=20, mutationRate=0.01, generations=10, GTA=GTA, BOARD=BOARD), BOARD)
        # moves = GTA.setupRoute(geneticAlgorithm.geneticAlgorithmPlot(population=list(BOARD.bins_places_taken), popSize=100, eliteSize=20, mutationRate=0.01, generations=500, GTA=GTA, BOARD=BOARD), BOARD)
        # moves = GTA.setupRoute(geneticAlgorithm.geneticAlgorithmPlot(population=list(BOARD.bins_places_taken), popSize=100, eliteSize=20, mutationRate=0.01, generations=1, GTA=GTA, BOARD=BOARD), BOARD)
        moves.reverse()
        chapter = 2

    # Generowanie obiektów stałych
    BOARD.drawConstantObjects(SCREEN)
    BOARD.drawTemporaryObjects(SCREEN)

    # Poruszanie się agenta po kliknięciu - krok co iterację (aż do wyczerpania elementów listy)
    if len(moves) != 0:
        item = moves.pop()
        GTA.direction = item[0].direction

        if GTA.direction == Direction.DOWN:
            GTA.image = GARBAGE_TRUCK_RESIZED_DOWN
        if GTA.direction == Direction.UP:
            GTA.image = GARBAGE_TRUCK_RESIZED_UP
        if GTA.direction == Direction.RIGHT:
            GTA.image = GARBAGE_TRUCK_RESIZED_RIGHT
        if GTA.direction == Direction.LEFT:
            GTA.image = GARBAGE_TRUCK_RESIZED_LEFT

        # Zmiana pozycji agenta
        GTA.changePosition(GTA.image.get_rect(center=BOARD.fields_list[item[0].x][item[0].y].fieldRect.center),
                           item[0].x, item[0].y, SCREEN, BOARD, GARBAGE_DUMP)

        if len(moves) == 0:
            print("[AGENT_STOP]: Agent zakończył kurs!")
            currTime = 0
            chapter = 1
            i += 1
            if i % 4 == 0:
                BOARD.isWinter = True
                BOARD.season = Season.WINTER
            elif i % 4 == 1:
                BOARD.isWinter = False
                BOARD.season = Season.SPRING
            elif i % 4 == 2:
                BOARD.isWinter = False
                BOARD.season = Season.SUMMER
            elif i % 4 == 3:
                BOARD.isWinter = False
                BOARD.season = Season.AUTUMN
            print("[SEASON]: Obecna pora roku to => {}.".format(BOARD.season.name))

    # Pętla eventów/wydarzeń
    for event in pygame.event.get():

        # Zakończenie programu
        if event.type == pygame.QUIT:
            run = False

    # Rysowanie agenta na planszy (zdjęcie, pozycja/koordynaty)
    SCREEN.blit(GTA.image, GTA.position)

    # Aktualizacja ekranu gry
    pygame.display.update()

# Zakończenie działania programu/gry
pygame.quit()
