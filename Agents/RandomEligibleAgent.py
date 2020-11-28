from Agent import *

class RandomEligibleAgent(Agent):

    def createGuess(self):
        # a less janky algorithm that just guesses any random code that hasn't already been guessed
        # and that is consistent with previous guesses -- Rosu (1999), according to the genetic algorithms paper
        output = Code([])
        while (output in self.environment.getGuessList()) or (not self.isConsistent(output)):
            output.randomize()
        return output