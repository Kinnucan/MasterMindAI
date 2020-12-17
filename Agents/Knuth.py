from Agent import *
from Code import *
from Clue import *


class Knuth(Agent):
    # Implements the 5-guess algorithm designed by Donald Knuth

    def __init__(self, gameManager, verbose=False, firstGuess = makeCode([1,1,2,2])):
        self.candidateCodes = generateAllCodes()
        self.allCodes = self.candidateCodes.copy()
        self.firstGuess = firstGuess
        Agent.__init__(self, gameManager, verbose=verbose, seeCode=False)


    # Removes a previously guessed code
    def removeGuessedCodes(self, codes, code):
        for i in codes:
            if (i == code.getPinList()):
                codes.remove(i)
                break

    # Creates a guess using Minimax scoring
    def createGuess(self, blackPegs, whitePegs, currGuess):
        self.removeBadCodes(blackPegs, whitePegs, currGuess)
        nextGuesses = self.miniMax()
        guess = self.getNextGuess(nextGuesses)
        return Code(guess)

    # For every code in candidateCodes, if it were the hidden code and did not give the same
    # number of black and white pegs in response to the current guess, then remove that code
    # from candidateCodes
    def removeBadCodes(self, blackPegs, whitePegs, currGuess):
        newCandidateCodes = []
        for i in self.candidateCodes:
            response = Code(i).getClue(currGuess)
            if response.getWhitePegs() == whitePegs and response.getBlackPegs() == blackPegs:
                newCandidateCodes.append(i)
        self.candidateCodes = newCandidateCodes.copy()

    # Implements the miniMax scoring algorithm
    def miniMax(self):
        scoreCount = {}
        score = {}
        nextGuesses = []
        for i in range(len(self.allCodes)):
            for j in range(len(self.candidateCodes)):
                currCode = Code(self.allCodes[i])
                pegs = currCode.getClue(Code(self.candidateCodes[j]))
                blackPegs = str(pegs.getBlackPegs())
                whitePegs = str(pegs.getWhitePegs())
                pegScore = blackPegs + whitePegs
                if (pegScore in scoreCount.keys()):
                    if (scoreCount[pegScore] > 0):
                        scoreCount[pegScore] += 1
                else:
                    scoreCount[pegScore] = 1
            max = self.getMaxScore(scoreCount)
            score[self.convertCode(self.allCodes[i])] = max
            scoreCount.clear()
        min = self.getMinScore(score)
        for item in score.items():
            if (item[1] == min):
                nextGuesses.append(item[0])
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
            currGuess = self.convertCode(guess)
            if (currGuess in self.candidateCodes):
                return currGuess
        for guess in nextGuesses:
            currGuess = self.convertCode(guess)
            if (currGuess in self.allCodes):
                return currGuess

    # Converts codes from list of CodePins to a string and vice versa
    def convertCode(self, code):
        if type(code[0]) == CodePin:
            codeSequence = ""
            for i in range(len(code)):
                codeSequence += code[i].getColor()
                codeSequence += " "
            return codeSequence
        elif type(code == str):
            pins = code.split()
            codeSequence = []
            for i in range(len(pins)):
                codeSequence.append(CodePin(pins[i]))
            return codeSequence

    # Runs the algorithm until the game is won
    def play(self):
        # currGuess = Code([CodePin("red"), CodePin("red"), CodePin("orange"), CodePin("orange")])
        # self.removeGuessedCodes(self.candidateCodes, currGuess)
        # self.removeGuessedCodes(self.allCodes, currGuess)
        # currResponse = self.environment.guessCode(currGuess)
        # if self.verbose:
        #     print("Guess:", currGuess, "Response:", currResponse)
        #
        # if (currResponse.isWinning()):
        #     print("Won in", self.environment.getGuessNumber(), "guesses!")
        # else:
        #     blackPegs = currResponse.getBlackPegs()
        #     whitePegs = currResponse.getWhitePegs()
        #     while True:
        #         currGuess = self.createGuess(blackPegs, whitePegs, currGuess)
        #         self.removeGuessedCodes(self.candidateCodes, currGuess)
        #         self.removeGuessedCodes(self.allCodes, currGuess)
        #         currResponse = self.environment.guessCode(currGuess)
        #         if self.verbose:
        #             print("Guess:", currGuess, "Response:", currResponse)
        #         if currResponse.isWinning():
        #             if self.verbose:
        #                 print("Won in", self.environment.getGuessNumber(), "guesses!")
        #             break
        #         blackPegs = currResponse.getBlackPegs()
        #         whitePegs = currResponse.getWhitePegs()
        #     return self.environment.getGuessNumber()

        currGuess = self.firstGuess
        while True:
            self.removeGuessedCodes(self.candidateCodes, currGuess)
            self.removeGuessedCodes(self.allCodes, currGuess)
            currResponse = self.environment.guessCode(currGuess)
            if self.verbose:
                print("Guess:", currGuess, "Response:", currResponse)
            if currResponse.isWinning():
                if self.verbose:
                    print("Won in", self.environment.getGuessNumber(), "guesses!")
                break
            blackPegs = currResponse.getBlackPegs()
            whitePegs = currResponse.getWhitePegs()
            currGuess = self.createGuess(blackPegs, whitePegs, currGuess)
        return self.environment.getGuessNumber()