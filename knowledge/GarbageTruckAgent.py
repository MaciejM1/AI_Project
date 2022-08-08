import os

import pygame
from images import *
from knowledge.RecyclingBin import BinType
from knowledge.GarbageDump import *
from knowledge.Sector import *
from knowledge.PathGenerator import *
import heapq
from neuralNet.neuralModel import prediction, transformer
from decisionTree.decisionTree import binDecision, dtree


class GarbageTruckAgent:
    def __init__(self, position, start_col, start_row, start_image):
        # Obecna kolumna pozycji
        self.col = start_col
        # Obecny wiersz pozycji
        self.row = start_row
        # Ikona [zmienia się w zależności od zwrotu]
        self.image = start_image
        # Kierunek/zwrot [zmienia się w zależności od poruszania góra/prawo/dół/lewo]
        self.direction = Direction.UP
        # Koordynaty [potrzebne do zmiany pozycji]
        self.position = position
        # Pojemność zbiornika paliwa [maksymalna, np. 1000 kroków]
        self.fuelTankCapacity = MAX_FUEL_TANK_CAPACITY
        # Aktualna ilość paliwa [0 - pusty bak, MAX - pełny bak | na start MAX - pełny bak]
        self.amountOfFuel = MAX_FUEL_TANK_CAPACITY
        # Komory śmieciarki
        # Tworzywa sztuczne i metale
        self.plastic_and_metal_chamber = GarbageChamber(ChamberType.PLASTIC_AND_METAL, MAX_CHAMBER_CAPACITY)
        # Szkło
        self.glass_chamber = GarbageChamber(ChamberType.GLASS, MAX_CHAMBER_CAPACITY)
        # Papier
        self.paper_chamber = GarbageChamber(ChamberType.PAPER, MAX_CHAMBER_CAPACITY)
        # Bio
        self.bio_chamber = GarbageChamber(ChamberType.BIO, MAX_CHAMBER_CAPACITY)

    def graphSearch(self, problem, plansza):
        fringe = []
        startNode = Node(problem.getStartState())
        startNode.state.direction = self.direction
        startNode.parent = startNode
        heapq.heappush(fringe, (problem.estimatedTotalCost(startNode), startNode))

        explored = set()

        def buildPathRecursive(path, lastElem):
            if lastElem.state is not problem.getStartState():
                path.append((lastElem.state, lastElem.action))
                return buildPathRecursive(path, lastElem.parent)
            path.reverse()
            return path

        def buildPathIterative(lastElem):
            path = []
            while lastElem.state is not problem.getStartState():
                path.append((lastElem.state, lastElem.action, lastElem.depth))
                lastElem = lastElem.parent
            path.reverse()
            return path

        while True:
            if len(fringe) == 0:
                return []
            elem = heapq.heappop(fringe)

            if problem.isGoalState(elem[1].state):
                #print("[EXPLORED_NODES]: Liczba eksplorowanych węzłów: ", len(explored))
                return buildPathIterative(elem[1])

            explored.add(elem[1])

            for state, action in problem.getSuccessors(elem[1], plansza):
                x = Node(state)
                x.parent = elem[1]
                x.action = action
                x.state.direction = problem.resolveDirection(elem[1].state.direction, action)
                x.depth = elem[1].depth + problem.fieldCost(state, plansza)
                x.estimatedCost = problem.estimatedTotalCost(x)

                if problem.checkFringe(fringe, state) and problem.checkExplored(explored, state):
                    heapq.heappush(fringe, (x.estimatedCost, x))
                else:
                    index = problem.inFringeWithPriority(fringe, x)
                    if index != -1:
                        heapq.heappush(fringe, (x.estimatedCost, x))

    # Funkcja odpowiedzialna za zmianę pozycji - DO TESTÓW
    def changePosition(self, position, col, row, screen, board, garbageDump):
        if (board.fields_list[col][row].blocked == False):
            screen.blit(GRASS_RESIZED, self.position)
            self.col = col
            self.row = row
            self.position = position
            if (
                    self.col == garbageDump.plastic_and_metal_sector.col and self.row == garbageDump.plastic_and_metal_sector.row):
                self.throwTrash(SectorType.PLASTIC_AND_METAL, garbageDump)
            elif (self.col == garbageDump.glass_sector.col and self.row == garbageDump.glass_sector.row):
                self.throwTrash(SectorType.GLASS, garbageDump)
            elif (self.col == garbageDump.paper_sector.col and self.row == garbageDump.paper_sector.row):
                self.throwTrash(SectorType.PAPER, garbageDump)
            elif (self.col == garbageDump.bio_sector.col and self.row == garbageDump.bio_sector.row):
                self.throwTrash(SectorType.BIO, garbageDump)
            elif (board.fields_list[self.col][self.row].fieldType == FieldType.FUEL_STATION_SECTOR):
                self.refueling()
            elif (board.fields_list[col][row].fieldType == FieldType.BIN_PLACE):
                self.collectRubbish(board)

    def refueling(self):
        if self.amountOfFuel != self.fuelTankCapacity:
            print("[FUEL_LEVEL]: Obecny stan paliwa: {}/{} jednostek.".format(self.amountOfFuel, self.fuelTankCapacity))
            print("[REFUELING]: Tankowanie ...")
            self.amountOfFuel = self.fuelTankCapacity
            print("[FUEL_FULL]: Zatankowano do pełna.")
            print("[FUEL_LEVEL]: Obecny stan paliwa: {}/{} jednostek.".format(self.amountOfFuel, self.fuelTankCapacity))

    # Odczytywanie ścieżki
    def resolvePath(self, start, path):
        print("[PATH_RESOLVE]: POZYCJA/STAN STARTOWY/POCZĄTKOWY: ({}, {}, {})".format(start.x, start.y,
                                                                                      printDirection(start.direction)))
        for state, action, cost in path:
            print(
                "[PATH_STEP]: {} -> ({}, {}, {}) <=> [OBECNY PONIESIONY KOSZT: {}]".format(printAction(action), state.x,
                                                                                           state.y, printDirection(
                        state.direction), cost))
        print()
        fullCost = path[len(path) - 1][2]
        self.amountOfFuel -= fullCost
        direction = path[len(path) - 1][0].direction
        print("[FUEL_LEVEL]: Obecny stan paliwa: {}/{} jednostek.".format(self.amountOfFuel, self.fuelTankCapacity))

        return (fullCost, direction)

    def setupRoute(self, route, board):
        moves = []
        cost = 0
        route.insert(0, (0, 5, Direction.UP))
        for i in range(len(route) - 1):
            problem = Problem(State(route[i][0], route[i][1], route[i][2]),
                                  State(route[i + 1][0], route[i + 1][1]))
            movesList = self.graphSearch(problem, board)
            if len(moves) != 0:
                fullCost, direction = self.resolvePath(moves[len(moves) - 1][0], movesList)
            else:
                fullCost, direction = self.resolvePath(State(0, 5, Direction.UP), movesList)
            moves = moves + movesList
            cost += fullCost
            route[i + 1] = (route[i + 1][0], route[i + 1][1], direction)
        n = len(route)
        route[n - 1] = (route[n - 1][0], route[n - 1][1], direction)
        route.append((4, 6))
        route.append((3, 6))
        route.append((2, 6))
        route.append((1, 6))
        route.append((0, 6))
        route.append((0, 5))
        for i in range(n - 1, len(route) - 1):
            problem = Problem(State(route[i][0], route[i][1], route[i][2]),
                              State(route[i + 1][0], route[i + 1][1]))
            movesList = self.graphSearch(problem, board)
            fullCost, direction = self.resolvePath(moves[len(moves) - 1][0], movesList)
            moves = moves + movesList
            cost += fullCost
            route[i + 1] = (route[i + 1][0], route[i + 1][1], direction)
        return moves

    def resolvePathForGeneticAlg(self, path):
        fullCost = path[len(path) - 1][2]
        direction = path[len(path) - 1][0].direction

        return (fullCost, direction)

    def resolveCost(self, path):
        fullCost = path[len(path) - 1][2]
        return fullCost

    # Zbieranie śmieci
    def collectRubbish(self, board):
        if board.fields_list[self.col][self.row].fieldObject != None and board.fields_list[self.col][
            self.row].fieldObject.binObject != None:
            result = prediction(os.getcwd() + board.fields_list[self.col][self.row].fieldObject.binObject.contentImage,
                                transformer)
            params = [0, 0, 0, 0, 0, 0, 0, 0]
            if board.fields_list[self.col][
                self.row].fieldObject.binObject.amountOfWaste >= MAX_BIN_CAPACITY / 2:
                params[2] = 1
            if board.fields_list[self.col][
                self.row].fieldObject.binObject.time >= LONG_TIME:
                params[3] = 1
            if board.fields_list[self.col][
                self.row].fieldObject.binObject.isQuality:
                params[4] = 1
            if board.home_list[board.fields_list[self.col][
                                   self.row].fieldObject.home - 1].isPaid:
                params[5] = 1
            if board.isWinter:
                params[6] = 1
            if board.fields_list[self.col][
                self.row].fieldObject.binObject.isBag:
                params[7] = 1
            if result == "plastic":
                print("[GARBAGE_ANALYSIS]: Śmieci sklasyfikowano jako TWORZYWA SZTUCZNE I METALE => (IMG: {}).".format(
                    board.fields_list[self.col][self.row].fieldObject.binObject.contentImage))
                if self.plastic_and_metal_chamber.amountOfWaste + board.fields_list[self.col][
                    self.row].fieldObject.binObject.amountOfWaste <= self.plastic_and_metal_chamber.capacity:
                    params[1] = 1
                print(
                    "[DECISION_PARAMETERS]: isBio={},isFreeSpace={},isEnough={},isLongTime={},isQuality={},isPaid={},isWinter={},isBag={}.".format(
                        params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7]))
                dec_res = binDecision(params, dtree)
                print("[DECISION_RESULT]: result={}.".format(dec_res))
                if dec_res:
                    print('[COLLECT_RUBBISH]: Zebrano odpadki typu TWORZYWA SZTUCZNE I METALE.')
                    self.plastic_and_metal_chamber.amountOfWaste += board.fields_list[self.col][
                        self.row].fieldObject.binObject.amountOfWaste
                    print('[CHAMBER_LEVEL]: Obecna ilość odpadków w komorze [TWORZYWA SZTUCZNE/METALE]: {}/{}'.format(
                        self.plastic_and_metal_chamber.amountOfWaste, self.plastic_and_metal_chamber.capacity))
                    board.fields_list[self.col][self.row].fieldObject.binObject = None
                    board.bins_places_taken.remove((self.col, self.row))
                    board.bins_places_free.add((self.col, self.row))
                else:
                    print(
                        '[COLLECT_RUBBISH_REFUSE]: Wykryto odpadki typu TWORZYWA SZTUCZNE I METALE, ale w agent uznał, że nie zabierze śmieci.')
                    if params[5] == 0:
                        print('[NO_PAYMENT]: Wywóz śmieci dla domu nr {} nie został opłacony!'.format(
                            board.fields_list[self.col][self.row].fieldObject.home))
                    elif params[4] == 0 and params[7] == 0:
                        print(
                            '[NO_QUALITY_AND_BAG]: Kosz na śmieci nie spełnia standardów jakości (nie ma uchwytu) oraz śmieci nie są w specjalnym worku.')
                        print(
                            '[NO_QUALITY_AND_BAG]: Aby śmieci zostały zabrane przynajmniej jedno z powyższych kryteriów musi być spełnione!')
                    elif params[1] == 0:
                        print(
                            '[NO_SPACE_IN_CHAMBER]: W śmieciarce zabrakło miejsca w komorze [TWORZYWA SZTUCZNE/METALE].')
                        print(
                            '[NO_SPACE_IN_CHAMBER]: Przepraszamy za problem. Śmieci zostaną odebrane wkrótce, jak to najszybciej możliwe.')
                    else:
                        print('[OTHER_PARAMS]: Śmieci nie zostały zabrane z powodów tajnych dla agenta.')
                        print('[OTHER_PARAMS]: Nie martw się, odbierzemy je wkrótce, w odpowiednim czasie.')
            elif result == "glass":
                print("[GARBAGE_ANALYSIS]: Śmieci sklasyfikowano jako SZKŁO => (IMG: {}).".format(
                    board.fields_list[self.col][self.row].fieldObject.binObject.contentImage))
                if self.glass_chamber.amountOfWaste + board.fields_list[self.col][
                    self.row].fieldObject.binObject.amountOfWaste <= self.glass_chamber.capacity:
                    params[1] = 1
                print(
                    "[DECISION_PARAMETERS]: isBio={},isFreeSpace={},isEnough={},isLongTime={},isQuality={},isPaid={},isWinter={},isBag={}.".format(
                        params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7]))
                dec_res = binDecision(params, dtree)
                print("[DECISION_RESULT]: result={}.".format(dec_res))
                if dec_res:
                    print('[COLLECT_RUBBISH]: Zebrano odpadki typu SZKŁO.')
                    self.glass_chamber.amountOfWaste += board.fields_list[self.col][
                        self.row].fieldObject.binObject.amountOfWaste
                    print('[CHAMBER_LEVEL]: Obecna ilość odpadków w komorze [SZKŁO]: {}/{}'.format(
                        self.glass_chamber.amountOfWaste, self.glass_chamber.capacity))
                    board.fields_list[self.col][self.row].fieldObject.binObject = None
                    board.bins_places_taken.remove((self.col, self.row))
                    board.bins_places_free.add((self.col, self.row))
                else:
                    print(
                        '[COLLECT_RUBBISH_REFUSE]: Wykryto odpadki typu SZKŁO, ale w agent uznał, że nie zabierze śmieci.')
                    if params[5] == 0:
                        print('[NO_PAYMENT]: Wywóz śmieci dla domu nr {} nie został opłacony!'.format(
                            board.fields_list[self.col][self.row].fieldObject.home))
                    elif params[4] == 0 and params[7] == 0:
                        print(
                            '[NO_QUALITY_AND_BAG]: Kosz na śmieci nie spełnia standardów jakości (nie ma uchwytu) oraz śmieci nie są w specjalnym worku.')
                        print(
                            '[NO_QUALITY_AND_BAG]: Aby śmieci zostały zabrane przynajmniej jedno z powyższych kryteriów musi być spełnione!')
                    elif params[1] == 0:
                        print(
                            '[NO_SPACE_IN_CHAMBER]: W śmieciarce zabrakło miejsca w komorze [SZKŁO].')
                        print(
                            '[NO_SPACE_IN_CHAMBER]: Przepraszamy za problem. Śmieci zostaną odebrane wkrótce, jak to najszybciej możliwe.')
                    else:
                        print('[OTHER_PARAMS]: Śmieci nie zostały zabrane z powodów tajnych dla agenta.')
                        print('[OTHER_PARAMS]: Nie martw się, odbierzemy je wkrótce, w odpowiednim czasie.')
            elif result == "paper":
                print("[GARBAGE_ANALYSIS]: Śmieci sklasyfikowano jako PAPIER => (IMG: {}).".format(
                    board.fields_list[self.col][self.row].fieldObject.binObject.contentImage))
                if self.paper_chamber.amountOfWaste + board.fields_list[self.col][
                    self.row].fieldObject.binObject.amountOfWaste <= self.paper_chamber.capacity:
                    params[1] = 1
                print(
                    "[DECISION_PARAMETERS]: isBio={},isFreeSpace={},isEnough={},isLongTime={},isQuality={},isPaid={},isWinter={},isBag={}.".format(
                        params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7]))
                dec_res = binDecision(params, dtree)
                print("[DECISION_RESULT]: result={}.".format(dec_res))
                if dec_res:
                    print('[COLLECT_RUBBISH]: Zebrano odpadki typu PAPIER.')
                    self.paper_chamber.amountOfWaste += board.fields_list[self.col][
                        self.row].fieldObject.binObject.amountOfWaste
                    print('[CHAMBER_LEVEL]: Obecna ilość odpadków w komorze [PAPIER]: {}/{}'.format(
                        self.paper_chamber.amountOfWaste, self.paper_chamber.capacity))
                    board.fields_list[self.col][self.row].fieldObject.binObject = None
                    board.bins_places_taken.remove((self.col, self.row))
                    board.bins_places_free.add((self.col, self.row))
                else:
                    print(
                        '[COLLECT_RUBBISH_REFUSE]: Wykryto odpadki typu PAPIER, ale w agent uznał, że nie zabierze śmieci.')
                    if params[5] == 0:
                        print('[NO_PAYMENT]: Wywóz śmieci dla domu nr {} nie został opłacony!'.format(
                            board.fields_list[self.col][self.row].fieldObject.home))
                    elif params[4] == 0 and params[7] == 0:
                        print(
                            '[NO_QUALITY_AND_BAG]: Kosz na śmieci nie spełnia standardów jakości (nie ma uchwytu) oraz śmieci nie są w specjalnym worku.')
                        print(
                            '[NO_QUALITY_AND_BAG]: Aby śmieci zostały zabrane przynajmniej jedno z powyższych kryteriów musi być spełnione!')
                    elif params[1] == 0:
                        print(
                            '[NO_SPACE_IN_CHAMBER]: W śmieciarce zabrakło miejsca w komorze [PAPIER].')
                        print(
                            '[NO_SPACE_IN_CHAMBER]: Przepraszamy za problem. Śmieci zostaną odebrane wkrótce, jak to najszybciej możliwe.')
                    else:
                        print('[OTHER_PARAMS]: Śmieci nie zostały zabrane z powodów tajnych dla agenta.')
                        print('[OTHER_PARAMS]: Nie martw się, odbierzemy je wkrótce, w odpowiednim czasie.')
            elif result == "bio":
                print("[GARBAGE_ANALYSIS]: Śmieci sklasyfikowano jako BIOODPADY => (IMG: {}).".format(
                    board.fields_list[self.col][self.row].fieldObject.binObject.contentImage))
                params[0] = 1
                if self.bio_chamber.amountOfWaste + board.fields_list[self.col][
                    self.row].fieldObject.binObject.amountOfWaste <= self.bio_chamber.capacity:
                    params[1] = 1
                print(
                    "[DECISION_PARAMETERS]: isBio={},isFreeSpace={},isEnough={},isLongTime={},isQuality={},isPaid={},isWinter={},isBag={}.".format(
                        params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7]))
                dec_res = binDecision(params, dtree)
                print("[DECISION_RESULT]: result={}.".format(dec_res))
                if dec_res:
                    print('[COLLECT_RUBBISH]: Zebrano odpadki typu BIOODPADY.')
                    self.bio_chamber.amountOfWaste += board.fields_list[self.col][
                        self.row].fieldObject.binObject.amountOfWaste
                    print('[CHAMBER_LEVEL]: Obecna ilość odpadków w komorze [BIOODPADY]: {}/{}'.format(
                        self.bio_chamber.amountOfWaste, self.bio_chamber.capacity))
                    board.fields_list[self.col][self.row].fieldObject.binObject = None
                    board.bins_places_taken.remove((self.col, self.row))
                    board.bins_places_free.add((self.col, self.row))
                else:
                    print(
                        '[COLLECT_RUBBISH_REFUSE]: Wykryto odpadki typu BIOODPADY, ale w agent uznał, że nie zabierze śmieci.')
                    if params[5] == 0:
                        print('[NO_PAYMENT]: Wywóz śmieci dla domu nr {} nie został opłacony!'.format(
                            board.fields_list[self.col][self.row].fieldObject.home))
                    elif params[4] == 0 and params[7] == 0:
                        print(
                            '[NO_QUALITY_AND_BAG]: Kosz na śmieci nie spełnia standardów jakości (nie ma uchwytu) oraz śmieci nie są w specjalnym worku.')
                        print(
                            '[NO_QUALITY_AND_BAG]: Aby śmieci zostały zabrane przynajmniej jedno z powyższych kryteriów musi być spełnione!')
                    elif params[1] == 0:
                        print(
                            '[NO_SPACE_IN_CHAMBER]: W śmieciarce zabrakło miejsca w komorze [BIOODPADY].')
                        print(
                            '[NO_SPACE_IN_CHAMBER]: Przepraszamy za problem. Śmieci zostaną odebrane wkrótce, jak to najszybciej możliwe.')
                    else:
                        print('[OTHER_PARAMS]: Śmieci nie zostały zabrane z powodów tajnych dla agenta.')
                        print('[OTHER_PARAMS]: Nie martw się, odbierzemy je wkrótce, w odpowiednim czasie.')
            # print(board.bins_places_free)
            # print(board.bins_places_taken)

    def throwTrash(self, sectorType, garbageDump):
        if sectorType == SectorType.PLASTIC_AND_METAL:
            garbageDump.plastic_and_metal_sector.amountOfWaste += self.plastic_and_metal_chamber.amountOfWaste
            print('[SECTOR_INFO]: Obecna ilość odpadków w sektorze [TWORZYWA SZTUCZNE/METALE]: ',
                  garbageDump.plastic_and_metal_sector.amountOfWaste)
            self.plastic_and_metal_chamber.amountOfWaste = 0
            print('[CHAMBER_LEVEL]: Obecna ilość odpadków w komorze [TWORZYWA SZTUCZNE/METALE]: {}/{}'.format(
                self.plastic_and_metal_chamber.amountOfWaste,
                self.plastic_and_metal_chamber.capacity))
        elif sectorType == SectorType.GLASS:
            garbageDump.glass_sector.amountOfWaste += self.glass_chamber.amountOfWaste
            print('[SECTOR_INFO]: Obecna ilość odpadków w sektorze [SZKŁO]: ',
                  garbageDump.glass_sector.amountOfWaste)
            self.glass_chamber.amountOfWaste = 0
            print('[CHAMBER_LEVEL]: Obecna ilość odpadków w komorze [SZKŁO]: {}/{}'.format(
                self.glass_chamber.amountOfWaste,
                self.glass_chamber.capacity))
        elif sectorType == SectorType.PAPER:
            garbageDump.paper_sector.amountOfWaste += self.paper_chamber.amountOfWaste
            print('[SECTOR_INFO]: Obecna ilość odpadków w sektorze [PAPIER]: ',
                  garbageDump.paper_sector.amountOfWaste)
            self.paper_chamber.amountOfWaste = 0
            print('[CHAMBER_LEVEL]: Obecna ilość odpadków w komorze [PAPIER]: {}/{}'.format(
                self.paper_chamber.amountOfWaste,
                self.paper_chamber.capacity))
        elif sectorType == SectorType.BIO:
            garbageDump.bio_sector.amountOfWaste += self.bio_chamber.amountOfWaste
            print('[SECTOR_INFO]: Obecna ilość odpadków w sektorze [BIO]: ',
                  garbageDump.bio_sector.amountOfWaste)
            self.bio_chamber.amountOfWaste = 0
            print('[CHAMBER_LEVEL]: Obecna ilość odpadków w komorze [BIO]: {}/{}'.format(self.bio_chamber.amountOfWaste,
                                                                                         self.bio_chamber.capacity))


class GarbageChamber:
    def __init__(self, chamberType, capacity):
        # Typ komory
        # 1 - komora na tworzywa sztuczne i metale
        # 2 - komora na szkło
        # 3 - komora na papier
        # 4 - komora na bioodpady
        self.chamberType = chamberType
        # Pojemność komory
        self.capacity = capacity
        # Ilość odpadów w komorze [na start 0]
        self.amountOfWaste = 0


class ChamberType(enumerate):
    PLASTIC_AND_METAL = 1,
    GLASS = 2,
    PAPER = 3,
    BIO = 4
