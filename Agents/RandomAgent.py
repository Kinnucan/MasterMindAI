from Agent import *

class RandomAgent(Agent):

    def createGuess(self):
        # a janky algorithm that just guesses any random code that hasn't already been guessed
        output = Code([])
        while output in self.environment.getGuessList():
            output.randomize()
        return output