import random
import numpy as np
import operator
import pandas as pd
import matplotlib.pyplot as plt
from knowledge.PathGenerator import *
from datetime import datetime


class Fitness:
    def __init__(self, route):
        self.route = route.copy()
        self.cost = 0
        self.fitness = 0.0

    def routeCost(self, GTA, BOARD):
        if self.cost == 0:
            routeCost = 0
            self.route.insert(0, (0, 5, Direction.UP))
            k = -1
            for i in range(len(self.route) - 1):
                problem = Problem(State(self.route[i][0], self.route[i][1], self.route[i][2]),
                                  State(self.route[i + 1][0], self.route[i + 1][1]))
                moves = GTA.graphSearch(problem, BOARD)
                fullCost, direction = GTA.resolvePathForGeneticAlg(moves)
                routeCost += fullCost
                self.route[i + 1] = (self.route[i + 1][0], self.route[i + 1][1], direction)
            self.cost = routeCost
        return self.cost

    def routeFitness(self, GTA, BOARD):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeCost(GTA, BOARD))
        return self.fitness


def generateRoute(binList):
    route = random.sample(binList, len(binList))
    return route


def initialPopulation(popSize, binList):
    population = []
    for i in range(popSize):
        population.append(generateRoute(binList))
    return population


def rankRoutes(population, GTA, BOARD):
    fitnessResults = {}
    for i in range(len(population)):
        # print(population[i])
        # print(type(population[i]))
        fitnessResults[i] = Fitness(population[i]).routeFitness(GTA, BOARD)
    return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)


def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index", "Fitness"])
    #print(df)
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

    for i in range(eliteSize):
        selectionResults.append(popRanked[i][0])

    for i in range(len(popRanked) - eliteSize):
        pick = 100 * random.random()
        for i in range(len(popRanked)):           
            if pick <= df.iat[i, 3]:
                selectionResults.append(popRanked[i][0])
                break

    return selectionResults


def matingPool(population, selectionResults):
    mating_pool = []
    for i in range(len(selectionResults)):
        index = selectionResults[i]
        mating_pool.append(population[index])
    return mating_pool


def breed(parentA, parentB):
    child = []
    childA = []
    childB = []

    genA = int(random.random() * len(parentA))
    genB = int(random.random() * len(parentA))

    startGen = min(genA, genB)
    endGen = max(genA, genB)

    for i in range(startGen, endGen):
        childA.append(parentA[i])

    childB = [item for item in parentB if item not in childA]
    child = childA + childB

    return child


def breedPopulation(mating_pool, eliteSize):
    children = []
    length = len(mating_pool) - eliteSize
    pool = random.sample(mating_pool, len(mating_pool))

    for i in range(eliteSize):
        children.append(mating_pool[i])

    for i in range(length):
        child = breed(pool[i], pool[len(mating_pool) - i - 1])
        children.append(child)
    return children


def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if random.random() < mutationRate:
            swapWith = int(random.random() * len(individual))

            field1 = individual[swapped]
            field2 = individual[swapWith]

            individual[swapped] = field2
            individual[swapWith] = field1

    return individual


def mutatePopulation(population, mutationRate):
    mutatedPop = []
    for i in range(len(population)):
        # print(population[i])
        # print(type(population[i]))
        mutateIndex = mutate(population[i], mutationRate)
        mutatedPop.append(mutateIndex)

    return mutatedPop


def nextGeneration(currentGen, eliteSize, mutationRate, GTA, BOARD):
    popRanked = rankRoutes(currentGen, GTA, BOARD)
    selectionResults = selection(popRanked, eliteSize)
    mating_pool = matingPool(currentGen, selectionResults)
    children = breedPopulation(mating_pool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)

    return nextGeneration


def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations, GTA, BOARD):
    pop = initialPopulation(popSize, population)
    print("Initial distance: " + str(1 / rankRoutes(pop, GTA, BOARD)[0][1]))

    for i in range(generations):
        print("Generation number: ", i)
        pop = nextGeneration(pop, eliteSize, mutationRate, GTA, BOARD)

    fitness = rankRoutes(pop, GTA, BOARD)
    fitness_max = fitness[0][1]
    for fit in fitness:
        if fit[0][1] == fitness_max:
            print(pop[fit[0][0]])
    print("Final distance: " + str(1 / rankRoutes()[0][1]))
    bestRouteIndex = rankRoutes(pop, GTA, BOARD)[0][0]
    bestRoute = pop[bestRouteIndex]
    print(bestRouteIndex)
    exit()
    


def geneticAlgorithmPlot(population, popSize, eliteSize, mutationRate, generations, GTA, BOARD):
    pop = initialPopulation(popSize, population)
    progress = []
    bs = rankRoutes(pop, GTA, BOARD)
    # print(bs)
    best_solution = 1 / bs[0][1]
    best_solution_index = bs[0][0]
    best_route = pop[best_solution_index]
    print("Koszt początkowy: " + str(best_solution))
    for i in range(generations):
        print("Generation number: ", i + 1, datetime.now().strftime("%d/%m/%y %H:%M"))
        pop = nextGeneration(pop, eliteSize, mutationRate, GTA, BOARD)
        bs = rankRoutes(pop, GTA, BOARD)
        if 1 / bs[0][1] < best_solution:
            best_solution = 1 / bs[0][1]
            best_solution_index = bs[0][0]
            best_route = pop[best_solution_index]
        progress.append(1 / bs[0][1])

    print("Koszt ostateczny: " + str(1 / bs[0][1]))
    bestRouteIndex = bs[0][0]
    bestRoute = pop[bestRouteIndex]
    print("Index:" + str(bestRouteIndex))
    print("Trasa: ", bestRoute)

    # fitness = rankRoutes(pop, GTA, BOARD)
    # print("FITNESS: " + str(fitness))
    # fitness_max = fitness[0][1]
    # for index, fit in fitness:
    #     if fit == fitness_max:
    #         print(pop[index])
    #
    # print("Koszt najlepszy: " + str(best_solution))
    # print("Index:" + str(best_solution_index))
    # print("Trasa: ", best_route)

    
    return best_route
