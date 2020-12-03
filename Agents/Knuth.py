from Agent import *
from GameManager import *
from CodePin import *
from Code import *
from itertools import permutations
from Clue import *


class Knuth:
    # Implements the 5-guess algorithm designed by Donald Knuth

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
            response = self.checkGuess([CodePin(i[0]), CodePin(i[1]), CodePin(i[2]), CodePin(i[3])])
            if (response.whitePegs != whitePegs or response.blackPegs != blackPegs):
                self.Set.remove(i)

    def checkGuess(self, guess):
        newClue = Clue()
        valid = True
        if str(type(guess)) != "<class 'Code.Code'>":
            print("The object provided is not a valid code.")
            valid = False
        elif len(guess.getPinList()) != PIN_NUMBER:
            print("The code provided is the wrong length.")
            valid = False
        if valid:
            newClue = self.environment.code.getClue(guess)
        return newClue

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