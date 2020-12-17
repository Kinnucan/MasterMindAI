from Agent import *

class LexicographicAgent(Agent):

    def __init__(self, gameManager, verbose=False, seeCode=False, firstGuess = makeCode([1,1,2,2])):
        Agent.__init__(self, gameManager, verbose, seeCode)
        self.firstGuess = firstGuess
        self.allCodes = [Code(pinlist) for pinlist in generateAllCodes()]
        self.numberOfCodes = len(self.allCodes)
        self.currentIndex = -1
        self.isFirstGuess = True

    def createGuess(self):
        # starts with a given first guess, then just guesses codes in lexicographic order (ignoring inconsistent codes)
        # Based on Swaszek (1999-2000)
        if self.isFirstGuess:
            self.isFirstGuess = False
            return self.firstGuess
        else:
            for i in range(self.currentIndex+1, self.numberOfCodes):
                codeToCheck = self.allCodes[i]
                if self.isConsistent(codeToCheck):
                    self.currentIndex = i
                    return codeToCheck