import random
import operator
import time
import math
from numpy import binary_repr
from utils import *

class geneticAlgorithm():
    def __init__(self, generations, populationSize, mutationRate, crossoverRate, interval):
        self.generations = generations
        self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate
        self.interval = interval
        self.quantityOfBits = math.ceil(math.log((self.interval[1] - self.interval[0]), 2.0))

    def initialPopulation(self):
        population = []
        for x in range(0, self.populationSize):
            number = random.randint(self.interval[0], self.interval[1])
            population.append([int(x) for x in list(binary_repr(number, self.quantityOfBits))]) # adiciona à população um individuo dentro do intervalo
        self.population = population

    def fitness(self, individual):
        number = binaryArrayToInt(individual, self.quantityOfBits)
        return ((number*number) - (3*number) + 4)

    def evaluatePopulation(self):
        self.evaluation = []
        for individual in self.population:
            self.evaluation.append(self.fitness(individual))

    def selection(self):
        tournamentParticipants = list(zip(self.population, self.evaluation))
        index = random.randint(0, self.populationSize-1)
        individual1 = tournamentParticipants[index]
        del tournamentParticipants[index]
        individual2 = tournamentParticipants[random.randint(0, self.populationSize-2)]
        if(individual1[1] > individual2[1]):
            return individual1[0]
        else:
            return individual2[0]

    def crossover(self, father, mother):
        child1 = father
        child2 = mother
        rand = random.random()
        if(rand <= self.crossoverRate):
            cutPoint = random.randint(0, self.quantityOfBits-1)
            child1 = father[:cutPoint] + mother[cutPoint:]
            child2 = father[cutPoint:] + mother[:cutPoint]
            child1 = self.fix(child1)
            child2 = self.fix(child2)
        return (child1, child2)

    def fix(self, binaryArray):
        quantityOfBits = len(binaryArray)
        number = binaryArrayToInt(binaryArray, quantityOfBits)
        if number < self.interval[0]:
            number = self.interval[0]
        elif number > self.interval[1]:
            number = self.interval[1]
        return [int(x) for x in list(binary_repr(number, quantityOfBits))]

    def bestChild(self):
        participants = list(zip(self.population, self.evaluation))
        return max(participants, key=lambda participant: participant[1]) #retorna o individuo com a melhor avaliação

    def start(self):
        self.initialPopulation()
        self.evaluatePopulation()
        for i in range(0,self.generations):
            print('Melhor filho da geração: ', self.bestChild())
            nextGeneration = []
            while(len(nextGeneration) < self.populationSize):
                father = self.selection()
                mother = self.selection()
                child1, child2 = self.crossover(father, mother)
                nextGeneration.append(child1)
                nextGeneration.append(child2)
            self.population = nextGeneration
            self.evaluatePopulation()
        print( 'Resultado: ', self.bestChild(),  )

def main():
    # generations = input('Quantidade de gerações: ')
    interval = [-10, 10] #resultado buscado em inteiro
    generations = 20
    populationSize = 30
    mutationRate = 0.01
    crossoverRate = 0.7

    ga = geneticAlgorithm(generations, populationSize, mutationRate, crossoverRate, interval)
    ga.start()
main()