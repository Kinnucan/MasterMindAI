# The manager of the Mastermind environment
from Code import *
from CodePin import *
from Clue import *


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
            newClue = self.code.getClue(guess)
        # add the clues for this guess to the list of all clues returned over the course of the game
        self.clueList.append(newClue)
        # add the guessed code to the list of all codes guessed
        self.guessList.append(guess)
        return newClue

    def getCode(self):
        return self.code

    def getGuessList(self):
        return self.guessList

    def getClueList(self):
        return self.clueList

    def getGuessNumber(self):
        return len(self.guessList)
