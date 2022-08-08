import pygame
from constants import *
from knowledge.Board import FieldType
from enum import Enum


# Klasa stanu
class State:
    def __init__(self, x, y, direction=None):
        self.x = x
        self.y = y
        self.direction = direction


# Klasa węzła
class Node:
    def __init__(self, state):
        self.state = state
        self.parent = None
        self.action = None
        self.depth = 0
        self.estimatedCost = 0

    # Operator porównania węzłów
    def __lt__(self, other):
        if self.estimatedCost < other.estimatedCost:
            return True
        return False


# Klasa problemu (definiuje parę stan początkowy - stan docelowy)
class Problem:
    def __init__(self, startState, goalState):
        self.startState = startState
        self.goalState = goalState

    # Funkcja następnika
    def getSuccessors(self, elem, BOARD):
        succ = []
        # ZWROT KU GÓRZE
        if elem.state.direction == Direction.UP:

            if elem.state.x < COLS - 1 and BOARD.fields_list[elem.state.x + 1][elem.state.y].blocked != True:
                succ.append((State(elem.state.x + 1, elem.state.y), Action.RIGHT))

            if elem.state.x > 0 and BOARD.fields_list[elem.state.x - 1][elem.state.y].blocked != True:
                succ.append((State(elem.state.x - 1, elem.state.y), Action.LEFT))

            if elem.state.y > 0 and BOARD.fields_list[elem.state.x][elem.state.y - 1].blocked != True:
                succ.append((State(elem.state.x, elem.state.y - 1), Action.UP))

        # ZWROT W PRAWO
        if elem.state.direction == Direction.RIGHT:

            if elem.state.x < COLS - 1 and BOARD.fields_list[elem.state.x + 1][elem.state.y].blocked != True:
                succ.append((State(elem.state.x + 1, elem.state.y), Action.UP))

            if elem.state.y > 0 and BOARD.fields_list[elem.state.x][elem.state.y - 1].blocked != True:
                succ.append((State(elem.state.x, elem.state.y - 1), Action.LEFT))

            if elem.state.y < ROWS - 1 and BOARD.fields_list[elem.state.x][elem.state.y + 1].blocked != True:
                succ.append((State(elem.state.x, elem.state.y + 1), Action.RIGHT))

        # ZWROT W LEWO
        if elem.state.direction == Direction.LEFT:

            if elem.state.x > 0 and BOARD.fields_list[elem.state.x - 1][elem.state.y].blocked != True:
                succ.append((State(elem.state.x - 1, elem.state.y), Action.UP))

            if elem.state.y > 0 and BOARD.fields_list[elem.state.x][elem.state.y - 1].blocked != True:
                succ.append((State(elem.state.x, elem.state.y - 1), Action.RIGHT))

            if elem.state.y < ROWS - 1 and BOARD.fields_list[elem.state.x][elem.state.y + 1].blocked != True:
                succ.append((State(elem.state.x, elem.state.y + 1), Action.LEFT))

        # ZWROT W DÓŁ
        if elem.state.direction == Direction.DOWN:
            if elem.state.x < COLS - 1 and BOARD.fields_list[elem.state.x + 1][elem.state.y].blocked != True:
                succ.append((State(elem.state.x + 1, elem.state.y), Action.LEFT))

            if elem.state.x > 0 and BOARD.fields_list[elem.state.x - 1][elem.state.y].blocked != True:
                succ.append((State(elem.state.x - 1, elem.state.y), Action.RIGHT))

            if elem.state.y < ROWS - 1 and BOARD.fields_list[elem.state.x][elem.state.y + 1].blocked != True:
                succ.append((State(elem.state.x, elem.state.y + 1), Action.UP))

        return succ

    # Funkcja sprawdzająca czy osiągnięto cel
    def isGoalState(self, state):
        if state.x == self.goalState.x and state.y == self.goalState.y:
            return True
        return False

    # Funkcja sprawdzająca czy osiągnięto cel w oparciu o heurystykę
    def isGoalStateHeuristic(self, state):
        if self.heuristic(state) == 0:
            return True
        return False

    def getStartState(self):
        return self.startState

    def getGoalState(self):
        return self.goalState

    # Funkcja sprawdzająca czy istnieje element w kolejce o danym stanie
    def checkFringe(self, fringe, state):
        for elem in fringe:
            if elem[1].state.x == state.x and elem[1].state.y == state.y:
                return False
        return True

    # Funkcja sprawdzający czy dany stan był już eksplorowany
    def checkExplored(self, explored, state):
        for elem in explored:
            if elem.state.x == state.x and elem.state.y == state.y and elem.state.direction == state.direction:
                return False
        return True

    def inFringeWithPriority(self, fringe, elem):
        for i in range(len(fringe)):
            if fringe[i][1].state.x == elem.state.x and fringe[i][1].state.y == elem.state.y:
                if fringe[i][1].estimatedCost > self.estimatedTotalCost(elem):
                    return i
        return -1

    def resolveDirection(self, direction, action):
        if direction == Direction.RIGHT:
            if action == Action.UP:
                return Direction.RIGHT
            if action == Action.LEFT:
                return Direction.UP
            if action == Action.RIGHT:
                return Direction.DOWN

        if direction == Direction.LEFT:
            if action == Action.UP:
                return Direction.LEFT
            if action == Action.LEFT:
                return Direction.DOWN
            if action == Action.RIGHT:
                return Direction.UP

        if direction == Direction.UP:
            if action == Action.UP:
                return Direction.UP
            if action == Action.LEFT:
                return Direction.LEFT
            if action == Action.RIGHT:
                return Direction.RIGHT

        if direction == Direction.DOWN:
            if action == Action.UP:
                return Direction.DOWN
            if action == Action.RIGHT:
                return Direction.LEFT
            if action == Action.LEFT:
                return Direction.RIGHT

    # Funkcja heurystyki
    def heuristic(self, state):
        # ODLEGŁOŚĆ MANHATTAN
        # JEŻELI 0 TO JESTEŚMY U CELU
        return abs(self.goalState.x - state.x) + abs(self.goalState.y - state.y)

    # Szacunkowy koszt całkowity do celu [koszt obecny + heurystyka]
    def estimatedTotalCost(self, node):
        return node.depth + self.heuristic(node.state)

    # Funkcja zwracająca koszt pola
    def fieldCost(self, state, BOARD):
        if BOARD.fields_list[state.x][state.y].fieldType == FieldType.BROKEN_ROAD:
            return BROKEN_ROAD_COST
        if BOARD.fields_list[state.x][state.y].fieldType == FieldType.MUD:
            return MUD_COST
        return GRASS_COST


class Action(Enum):
    UP = 1,
    RIGHT = 2,
    DOWN = 3,
    LEFT = 4


def printAction(action):
    if action == Action.UP:
        return "DO PRZODU"
    if action == Action.RIGHT:
        return "W PRAWO"
    if action == Action.DOWN:
        return "DÓŁ"
    if action == Action.LEFT:
        return "W LEWO"
    if action == "POZYCJA STARTOWA":
        return "POZYCJA STARTOWA"


def printDirection(direction):
    if direction == Direction.UP:
        return "GÓRA"
    if direction == Direction.RIGHT:
        return "PRAWO"
    if direction == Direction.DOWN:
        return "DÓŁ"
    if direction == Direction.LEFT:
        return "LEWO"


class Direction(Enum):
    UP = 1,
    RIGHT = 2,
    DOWN = 3,
    LEFT = 4
