# The manager of the Mastermind environment
from MasterMind.Code import *
from MasterMind.CodePin import *


class Clue:
    def __init__(self, blackPegs = 0, whitePegs = 0):
        self.blackPegs = blackPegs
        self.whitePegs = whitePegs

    def getBlackPegs(self):
        return self.blackPegs

    def getWhitePegs(self):
        return self.whitePegs

    def augmentBlackPegs(self):
        self.blackPegs+=1

    def augmentWhitePegs(self):
        self.whitePegs+=1

    def isWinning(self):
        return self.blackPegs >= PIN_NUMBER

    def __str__(self):
        return str(self.blackPegs) + " black, " + str(self.whitePegs) + " white"


class GameManager:

    def __init__(self, code = Code([])):
        # the hidden code
        self.code = code
        # the list of all codes guessed over the course of the game
        self.guessList = []
        # the list of all clues returned over the course of the game
        self.clueList = []


    # generate a randomized code
    def generateCode(self):
        self.code = Code([])

    # process a guess (each guess will be compared with the manager's existing Code)
    def guessCode(self, guess):
        newClue = Clue()
        valid = True
        if str(type(guess)) != "<class 'Code.Code'>":
            print("The object provided is not a valid code.")
            valid = False
        elif len(guess.getPinList()) != PIN_NUMBER:
            print("The code provided is the wrong length.")
            valid = False
        if valid:
            # check every pin to see if there are any exact (i.e., black) matches
            for i in range(PIN_NUMBER):
                codePin = self.code.getPinList()[i]
                guessPin = guess.getPinList()[i]
                if codePin == guessPin:
                    # add a "black pin" to the clue to indicate a perfect match exists
                    newClue.augmentBlackPegs()
                    # denote the pins as having been matched
                    guessPin.match()
                    codePin.match()
            # check every pin in the hidden code to see if there are any inexact (i.e., white) matches
            for codeInd in range(PIN_NUMBER):
                codePin = self.code.getPinList()[codeInd]
                # run through all of the pins in the guess
                for guessInd in range(PIN_NUMBER):
                    guessPin = guess.getPinList()[guessInd]
                    # if the pin has been previously matched, skip over it. Otherwise, check it
                    if not (guessPin.matched or codePin.matched):
                        if codePin == guessPin:
                            if codeInd != guessInd:
                                # add a "white pin" to the clue list to indicate correct color, but wrong position
                                newClue.augmentWhitePegs()
                                # denote the pins as having been matched
                                guessPin.match()
                                codePin.match()
        # we don't need the matchings anymore
        guess.cleanMatches()
        self.code.cleanMatches()
        # add the clues for this guess to the list of all clues returned over the course of the game
        self.clueList.append(newClue)
        # add the guessed code to the list of all codes guessed
        self.guessList.append(guess)
        return newClue

    def getCode(self):
        return self.code

    def getGuessList(self):
        return self.guessList

    def getGuessNumber(self):
        return len(self.guessList)
