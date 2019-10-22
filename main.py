import random
import operator
import time
import math
from numpy import binary_repr
from utils import *

class geneticAlgorithm():
    def __init__(self, generations, populationSize, mutationRate, crossoverRate, interval, a, b, c, isMax):
        self.generations = generations
        self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate
        self.interval = interval
        self.quantityOfBits = math.ceil(math.log((self.interval[1] - self.interval[0]), 2.0))
        self.a = a
        self.b = b
        self.c = c
        self.isMax = isMax

    def initialPopulation(self):
        population = []
        for x in range(0, self.populationSize):
            number = random.randint(self.interval[0], self.interval[1])
            population.append([int(x) for x in list(binary_repr(number, self.quantityOfBits))]) # adiciona à população um individuo dentro do intervalo
        self.population = population

    def fitness(self, individual):
        number = binaryArrayToInt(individual, self.quantityOfBits)
        return ((self.a*(number*number)) + (self.b*number) + self.c)

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
        if(self.isMax):
            if(individual1[1] > individual2[1]):
                return individual1[0]
            else:
                return individual2[0]
        else :
            if(individual1[1] < individual2[1]):
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
        if(self.isMax):
            return max(participants, key=lambda participant: participant[1]) #retorna o individuo com a melhor avaliação
        else:
            return min(participants, key=lambda participant: participant[1]) #retorna o individuo com a melhor avaliação

    def mutation(self, individual):
        number = binaryArrayToInt(individual, self.quantityOfBits)
        if(random.random() <= self.mutationRate):
            number = (number * -1)
        return [int(x) for x in list(binary_repr(number, self.quantityOfBits))] 

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
                child1 = self.mutation(child1)
                child2 = self.mutation(child2)
                nextGeneration.append(child1)
                nextGeneration.append(child2)
            self.population = nextGeneration
            self.evaluatePopulation()

        bestChild = self.bestChild()
        print('------------------------------------------------')
        print('Melhor indivíduo:', bestChild)
        individual, y = bestChild
        if(self.isMax):
            print('X máximo:', binaryArrayToInt(bestChild[0], self.quantityOfBits), '\nY máximo: ', y )
        else:
            print('X mínimo:', binaryArrayToInt(bestChild[0], self.quantityOfBits), '\nY mínimo: ', y )


def main():
    option = input('1) Executar com valores padrões \n2) Executar com valores personalizados\n')
    isMax = True
    print('------------------------------------------------')
    if(option == '1'):
        interval = [-10, 10] #intervalo de busca
        generations = 20
        populationSize = 30
        mutationRate = 0.01
        crossoverRate = 0.7
        a = 1
        b = -3
        c = 4
    else:
        option2 = input('1)Procurar por ponto máximo \n2)Procurar por ponto mínimo\n')
        if(option2 == '2'):
            isMax= False
        print('Valores padrões entre parenteses:')
        a = float(input('Valor do "a" da função(1): '))
        b = float(input('Valor do "b" da função(-3): '))
        c = float(input('Valor do "c" da função(4): '))
        generations = int(input('Quantidade de gerações(20): '))
        intervalMin = int(input('Valor mínimo do intervalo de busca(-10): '))
        intervalMax = int(input('Valor máximo do intervalo de busca(10): '))
        interval = [intervalMin, intervalMax]
        populationSize = int(input('Tamanho da população(30): '))
        mutationRate = float(input('Taxa de mutação(0.01): '))
        crossoverRate = float(input('Taxa de crossover(0.7): '))

    print('------------------------------------------------')

    ga = geneticAlgorithm(generations, populationSize, mutationRate, crossoverRate, interval, a, b, c, isMax)
    ga.start()
main()