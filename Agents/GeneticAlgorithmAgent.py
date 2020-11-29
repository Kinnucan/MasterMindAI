from Agent import *

class GeneticAlgorithmAgent(Agent):
    #implements the genetic algorithm proposed by Berghman, Goossens, and Leus

    def __init__(self, gameManager, verbose=False, seeCode=False, firstGuess = makeCode([1]*PIN_NUMBER), popSize = 150, maxGen = 100, maxSize = 60,
                 onePointCrossoverProb = .5, colorChangeProb = .03, permutationProb = .03, inversionProb = .02, a = 1, b = 2, EHatChoiceMethod = "min"):
        Agent.__init__(self, gameManager, verbose, seeCode)
        self.firstGuess = firstGuess # the paper recommends (1,1,2,3) -- "red red orange yellow" -- as an ideal first guess
        self.popSize = popSize # the size of the initial population
        self.maxGen = maxGen # how many generations we go through
        self.maxSize = maxSize # how many eligible codes we consider after each use of the genetic algorithm

        self.guessNumber = 1


    def createGuess(self):
        if self.guessNumber == 1:
            return self.firstGuess
        currentGen = 1
        EHat = []  # the set of eligible combinations created
        population = self.initializePopulation()
        while currentGen <= self.maxGen and len(EHat) <= self.maxSize:
            population = self.makeNewPopulation(population)
            for code in population:
                if self.isConsistent(code):
                    EHat.append(code)
            currentGen += 1
        return self.chooseFromEHat(EHat)



    def initializePopulation(self):
        output = []
        for i in range(self.popSize):
            newCode = Code([])
            while newCode in output:
                newCode.randomize()
            output.append(newCode)
        return output

    def makeNewPopulation(self, pop):
        output = self.crossover(pop)
        output = self.mutate(output)
        return output

    def crossover(self, pop):
        return pop

    def mutate(self, pop):
        return pop

    def fitness(self, code):
        return 1

    def chooseFromEHat(self, possibleCodes):
        return None