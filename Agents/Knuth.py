from Agent import *
from GameManager import *
from CodePin import *
from Code import *
from itertools import permutations
from Clue import *


class Knuth:
    # Implements the 5-guess algorithm designed by Donald Knuth

    def __init__(self, gameManager):
        self.candidateCodes = self.generateCodes()
        self.allCodes = self.candidateCodes.copy()
        Agent.__init__(self, gameManager, verbose=True, seeCode=False)

    # Generates the set of all possible codes
    def generateCodes(self):
        colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        setOfCodes = []
        permutation = [None, None, None, None]

        for a in colors:
            permutation[0] = CodePin(a)
            for b in colors:
                permutation[1] = CodePin(b)
                for c in colors:
                    permutation[2] = CodePin(c)
                    for d in colors:
                        permutation[3] = CodePin(d)
                        setOfCodes.append(permutation)
        return setOfCodes

    # Removes a previously guessed code
    def removeGuessedCodes(self, codes, code):
        for i in range(len(codes)):
            if (Code(codes[i]).getPinList() == code.getPinList()):
                codes.remove(i)

    # Creates a guess using Minimax scoring
    def createGuess(self, blackPegs, whitePegs):
        self.removeBadCodes(blackPegs, whitePegs)
        nextGuesses = self.miniMax()
        guess = self.getNextGuess(nextGuesses)
        return guess

    # Removes codes that wouldn't give the same number of black and white pegs
    def removeBadCodes(self, blackPegs, whitePegs):
        for i in self.candidateCodes:
            response = self.processGuess(Code(i))
            if (response.whitePegs != whitePegs or response.blackPegs != blackPegs):
                self.candidateCodes.remove(i)

    # Processes a guess and returns the number of black and white pegs as a Clue object
    def processGuess(self, guess):
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

    # Implements the miniMax scoring algorithm
    def miniMax(self):
        scoreCount = {}
        score = {}
        nextGuesses = []
        for i in range(len(self.allCodes)):
            for j in range(len(self.candidateCodes)):
                currCode = self.allCodes[i]
                pegScore = currCode.getClue(self.candidateCodes[j])
                if (scoreCount[pegScore] > 0):
                    scoreCount[pegScore] += 1
                else:
                    scoreCount[pegScore] = 1
            max = self.getMaxScore(scoreCount)
            score[self.allCodes[i]] = max
            scoreCount.clear()
        min = self.getMinScore(score)
        for code, val in score:
            if (val == min):
                nextGuesses.append(code)
        return nextGuesses

    # Gets the maximum score from the dictionary
    def getMaxScore(self, map):
        max = 0
        for value in map.values():
            if (value > max):
                max = value
        return max

    # Gets the minimum score from the dictionary
    def getMinScore(self, map):
        min = 10000000
        for value in map.values():
            if (value < min):
                min = value
        return min

    # Gets the next guess from the list of possible next guesses, using one from candidateCodes whenever possible
    def getNextGuess(self, nextGuesses):
        for guess in nextGuesses:
            if (guess in self.candidateCodes):
                return guess
        for guess in nextGuesses:
            if (guess in self.allCodes):
                return guess

    # Runs the algorithm until the game is won
    def play(self):
        initialGuess = Code([CodePin("red"), CodePin("red"), CodePin("orange"), CodePin("orange")])
        self.removeGuessedCodes(self.candidateCodes, initialGuess)
        self.removeGuessedCodes(self.allCodes, initialGuess)
        initialResponse = self.environment.guessCode(initialGuess)

        if (initialResponse.isWinning()):
            print("Won in", self.environment.getGuessNumber(), "guesses!")
        else:
            blackPegs = initialResponse.getBlackPegs()
            whitePegs = initialResponse.getWhitePegs()
            while True:
                newGuess = self.createGuess(blackPegs, whitePegs)
                self.removeGuessedCodes(self.candidateCodes, newGuess)
                self.removeGuessedCodes(self.allCodes, newGuess)
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