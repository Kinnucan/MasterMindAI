from Agents.RandomAgent import *
from Agents.HumanAgent import *
from Agents.Knuth import *
from Agents.RandomEligibleAgent import *
from Agents.Player import *
from Agents.GeneticAlgorithmAgent import *
import time



def doKnuthTests(numberOfTrials, firstGuess = makeCode([1,1,2,2])):
    guessesNeeded = 0
    timeNeeded = 0
    print("Trial Number: ", end="")
    for i in range(numberOfTrials):
        if i % 10 == 0:
            print(i+1, end=" ")
        newGame = GameManager()
        newGame.generateCode()
        knuth = Knuth(newGame, firstGuess = firstGuess)
        start = time.time()
        guessesNeeded += knuth.play()
        timeNeeded += time.time()-start
    print()
    print("Average guesses needed:", guessesNeeded/numberOfTrials)
    print("Average time needed:", timeNeeded/numberOfTrials)

def doGeneticTests(numberOfTrials, verbose=False, seeCode=False, firstGuess = makeCode([1]*PIN_NUMBER), popSize = 150, maxGen = 100, maxSize = 60,
                 onePointCrossoverProb = .5, colorChangeProb = .03, permutationProb = .03, inversionProb = .02, a = 1, b = 2, EHatChoiceMethod = "min",
                 fitnessMethod = "changed"):
    guessesNeeded = 0
    timeNeeded = 0
    print("Trial Number: ", end="")
    for i in range(numberOfTrials):
        if i % 1 == 0:
            print(i+1, end=" ")
        newGame = GameManager()
        newGame.generateCode()
        genny = GeneticAlgorithmAgent(newGame, verbose, seeCode, firstGuess, popSize, maxGen, maxSize, onePointCrossoverProb, colorChangeProb, permutationProb, inversionProb, a, b, EHatChoiceMethod, fitnessMethod)
        start = time.time()
        guessesNeeded += genny.play()
        timeNeeded += time.time()-start
    print()
    print("Average guesses needed:", guessesNeeded / numberOfTrials)
    print("Average time needed:", timeNeeded / numberOfTrials)


print("Knuth algorithm:")
doKnuthTests(500)
print("Genetic algorithm:")
doGeneticTests(100, firstGuess=makeCode([1,1,2,3]))
print("Genetic algorithm (speedier):")
doGeneticTests(100, firstGuess=makeCode([1,1,2,3]), EHatChoiceMethod="random", maxGen=150)
print("Genetic algorithm (with old fitness method):")
doGeneticTests(100, firstGuess=makeCode([1,1,2,3]), fitnessMethod="original", EHatChoiceMethod="random")
