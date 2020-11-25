from Agent import *
from GameManager import *
from CodePin import *
from Code import *
from itertools import permutations


class Knuth:

    def __init__(self, gameManager):
        Agent.__init__(self, gameManager, verbose=True, seeCode=False)

    def createGuess(self):

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

    def play(self):
        initialGuess = Code([CodePin("red"), CodePin("red"), CodePin("orange"), CodePin("orange")])
        initialResponse = self.environment.guessCode(initialGuess)

        # ADD IF STATEMENT CHECKING IF RESPONSE IS FOUR COLORED PEGS