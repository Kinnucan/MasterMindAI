import random
from Agent import *
from GameManager import *
from CodePin import *
from Code import *


# choose a color randomly from a given list
# used when the agent is testing out a single color
def randomColor(viableColors):
    color = random.choice(viableColors)
    return color


# choose two different colors randomly from a given list
def randomTwoColors(viableColors):
    if len(viableColors) > 2:
        clist = viableColors
        color1 = randomColor(clist)
        clist.remove(color1)
        color2 = randomColor(clist)
        return color1, color2


"""A class that replicates a human strategy of playing through MasterMind."""


class HumanAgent(Agent):
    COLOR_LIST = ["red", "orange", "yellow", "green", "blue", "purple"]

    def __init__(self, gameManager):
        self.environment = gameManager
        self.guessList = self.environment.getGuessList()
        self.clueList = self.environment.getClueList()
        self.guess = []
        self.guessCount = 0
        self.viableColors = self.COLOR_LIST
        self.testRound = 0  # changes how the agent plays (from gathering information to acting on that information)

    def createGuess(self):
        self.guessList = self.environment.getGuessList()
        self.clueList = self.environment.getClueList()
        # a temporary list used to narrow down color choices for a single guess
        clist = self.viableColors
        # first phase: keep guessing until you receive at least one clue in return
        if self.testRound == 0:
            color1, color2 = randomTwoColors(self.viableColors)
            self.guess = Code([CodePin(color1), CodePin(color1), CodePin(color2), CodePin(color2)])
        # second phase: switch out one color to see how it affects the given clue
        else:
            if self.testRound == 1:
                # at this point, any previous guesses will have only been made with two colors
                prevColors = self.guess.getColors()
                prevColor1 = prevColors[0]
                prevColor2 = prevColors[1]
                clist.remove(prevColor1)
                clist.remove(prevColor2)
                # choose a new, as of yet unused color to insert into the guess
                newColor = randomColor(clist)
                # choose one of the previous colors to reuse, and replace the other color with the new selection
                if random.randint(0, 1) == 0:
                    self.guess = Code([CodePin(prevColor1), CodePin(prevColor1), CodePin(newColor), CodePin(newColor)])
                else:
                    self.guess = Code([CodePin(newColor), CodePin(newColor), CodePin(prevColor2), CodePin(prevColor2)])
            else:
                if self.testRound == 2:
                    # retrieve the clue given after the last round
                    lastClue = self.clueList[self.guessCount]
                    # TODO: Before continuing, test this out

