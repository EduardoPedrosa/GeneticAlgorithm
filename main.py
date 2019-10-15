import random
import operator
import time
import math
from numpy import binary_repr

class geneticAlgorithm():
    def __init__(self, generations, populationSize, mutationRate, crossoverRate, interval):
        self.generations = generations
        self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate
        self.interval = interval

    def initialPopulation(self):
        individualSize = math.log((self.interval[1] - self.interval[0]), 2.0)
        quantityOfBits = math.ceil(individualSize)
        population = []
        for x in range(0, self.populationSize):
            number = random.randint(self.interval[0], self.interval[1])
            population.append([int(x) for x in list(binary_repr(number, quantityOfBits))]) # adiciona à população um individuo dentro do intervalo
        return population

    #def fitness(self):



def main():
    # generations = input('Quantidade de gerações: ')
    interval = [-10, 10] #resultado buscado em inteiro
    generations = 20
    populationSize = 30
    mutationRate = 0.01
    crossoverRate = 0.7

    ga = geneticAlgorithm(generations, populationSize, mutationRate, crossoverRate, interval)
    initialPopulation = ga.initialPopulation()
    arrayInString = (''.join(str(x) for x in initialPopulation[0])) #exemplo de transformação de um array de bits em string
    
main()