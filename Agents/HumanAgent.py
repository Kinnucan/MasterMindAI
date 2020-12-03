from Agent import *

class HumanAgent(Agent):

    def __init__(self, gameManager):
        Agent.__init__(self, gameManager, verbose=True, seeCode=False)

    def createGuess(self):
        # a janky algorithm that just guesses any random code that hasn't already been guessed
        guessString = input("What's your guess? > ")
        guess = Code([CodePin(word) for word in guessString.split()])
        return guess