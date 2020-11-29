from Agent import *
from GameManager import *
from CodePin import *
from Code import *
from itertools import permutations


class Knuth:

    def __init__(self, gameManager):
        self.Set = self.generateSet()
        Agent.__init__(self, gameManager, verbose=True, seeCode=False)

    def createGuess(self, blackPegs, whitePegs):
        return 0

    def generateSet(self):
        colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        setOfCodes = []
        permutation = [None, None, None, None]

        for a in colors:
            permutation[0] = a
            for b in colors:
                permutation[1] = b
                for c in colors:
                    permutation[2] = c
                    for d in colors:
                        permutation[3] = d
                        setOfCodes.append(permutation)
        return setOfCodes

    def miniMax(self):
        return 0

    def play(self):
        initialGuess = Code([CodePin("red"), CodePin("red"), CodePin("orange"), CodePin("orange")])
        initialResponse = self.environment.guessCode(initialGuess)

        blackPegs = initialResponse.getBlackPegs()
        whitePegs = initialResponse.getWhitePegs()

        if (initialResponse.isWinning()):
            print("Won in", self.environment.getGuessNumber(), "guesses!")
        else:
            while True:
                newGuess = self.createGuess(blackPegs, whitePegs)
                newResponse = self.environment.guessCode(newGuess)
                if self.verbose:
                    print("Guess:", newGuess, "Response:", newResponse)
                if newResponse.isWinning():
                    if self.verbose:
                        print("Won in", self.environment.getGuessNumber(), "guesses!")
                    break
                blackPegs = newResponse.getBlackPegs()
                whitePegs = newResponse.getWhitePegs()
            return self.environment.getGuessNumber()