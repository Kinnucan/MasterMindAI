from Agent import *

class GeneticAlgorithmAgent(Agent):
    #implements the genetic algorithm proposed by Berghman, Goossens, and Leus

    def __init__(self, gameManager, verbose=False, seeCode=False, firstGuess = makeCode([1]*PIN_NUMBER), popSize = 150, maxGen = 100, maxSize = 60):
        Agent.__init__(self, gameManager, verbose, seeCode)
        self.firstGuess = firstGuess # the paper recommends (1,1,2,3) -- "red red orange yellow" -- as an ideal first guess
        self.popSize = popSize # the size of the initial population
        self.maxGen = maxGen # how many generations we go through
        self.maxSize = maxSize # how many eligible codes we consider after each use of the genetic algorithm

        self.guessNumber = 1
        self.currentGen = 1
        self.EHat = [] # the set of eligible combinations created


    def createGuess(self):
        if self.guessNumber == 1:
            return self.firstGuess
        self.currentGen = 1
        self.EHat = []
        population = self.initializePopulation()


    def initializePopulation(self):
        return []

