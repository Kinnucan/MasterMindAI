from GameManager import *
from CodePin import *
from Code import *


def isConsistent(guess, prevGuesses, prevClues):
    # checks if a guess is consistent with the evidence
    for i in range(len(prevGuesses)):
        if guess.getClue(prevGuesses[i]) != prevClues[i]:
            return False
    return True


class Agent:
    #an abstract class for making agents
    def __init__(self, gameManager, verbose=False, seeCode=False):
        self.environment = gameManager
        self.verbose = verbose
        if seeCode:
            print("The secret code is", gameManager.getCode())

    def createGuess(self):
        # given the current state of the environment (which includes the agent's percept history --
        # its previous guesses and their responses -- due to the way we've coded it), guess a new code!
        return None

    def play(self):
        while True:
            newGuess = self.createGuess()
            newResponse = self.environment.guessCode(newGuess)
            if self.verbose:
                print("Guess:", newGuess, "Response:", newResponse)
            if newResponse.isWinning():
                if self.verbose:
                    print("Won in", self.environment.getGuessNumber(), "guesses!")
                break
        return self.environment.getGuessNumber()

    # ============================================
    # some helper function(s) for agents
    # ============================================
    def isConsistent(self, guess):
        return isConsistent(guess, self.environment.getGuessList(), self.environment.getClueList())


