from Agent import *
from GameManager import *
from CodePin import *
from Code import *
from itertools import permutations


class Knuth:

    def __init__(self, gameManager):
        self.Set = self.generateSet()
        Agent.__init__(self, gameManager, verbose=True, seeCode=False)

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

    def createGuess(self, blackPegs, whitePegs):
        self.removeCodes(blackPegs, whitePegs)
        guess = self.miniMax()
        return guess

    def removeCodes(self, blackPegs, whitePegs):
        for i in self.Set:
            # You'll need to modify this to be similar to the first line of code under the play function
            response = self.checkGuess(i)
            if (response.whitePegs != whitePegs or response.blackPegs != blackPegs):
                self.Set.remove(i)

    def checkGuess(self, guess):
        # Implement code here similar to that of guessCode in GameManager.py
        # You'll want it to check if the guess produces the same number of white pegs and black pegs, but without
        # changing the state of the actual game
        return 0

    def miniMax(self):
        return 0

    def play(self):
        initialGuess = Code([CodePin("red"), CodePin("red"), CodePin("orange"), CodePin("orange")])
        initialResponse = self.environment.guessCode(initialGuess)

        if (initialResponse.isWinning()):
            print("Won in", self.environment.getGuessNumber(), "guesses!")
        else:
            blackPegs = initialResponse.getBlackPegs()
            whitePegs = initialResponse.getWhitePegs()
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