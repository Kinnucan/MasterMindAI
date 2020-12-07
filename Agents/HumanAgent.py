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
        clist = viableColors.copy()
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
        self.won = False

    def createGuess(self):
        self.guessList = self.environment.getGuessList()
        self.clueList = self.environment.getClueList()
        # a temporary list used to narrow down color choices for a single guess
        clist = self.viableColors.copy()
        # analyze the most recent clue, if there is one (empty clues count)
        if self.guessCount > 0:
            result = self.analyzeLatestClue()
        # first phase: keep guessing until you receive at least one clue in return
        print("testRound is: " + str(self.testRound))
        if self.testRound == 0:
            color1, color2 = randomTwoColors(clist)
            clist.remove(color1)
            clist.remove(color2)
            newGuess = Code([CodePin(color1), CodePin(color1), CodePin(color2), CodePin(color2)])
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
                    newGuess = Code([CodePin(prevColor1), CodePin(prevColor1), CodePin(newColor), CodePin(newColor)])
                else:
                    newGuess = Code([CodePin(newColor), CodePin(newColor), CodePin(prevColor2), CodePin(prevColor2)])
            else:
                if self.testRound == 2:
                    # retrieve the clue given after the last round
                    lastClue = self.clueList[self.guessCount]
        # update the guess list
        self.guessList.append(newGuess)
        self.guess = newGuess
        self.guessCount += 1
        print("The agent's guess is: " + self.guess.__str__())

    def analyzeLatestClue(self):
        clue = self.clueList[self.guessCount-1]

        # check to see if the game has been won; if so, end the method
        if clue.getBlackPegs() == 4:
            self.won = True
            return True
        # if in phase 1...
        if self.testRound == 0:
            # if the guess got any feedback, move to phase 2
            if clue.hasPegs():
                self.testRound += 1
            return True
        # if in phase 2...
        else:
            if self.testRound == 1:
                # automatically move to phase 3
                self.testRound += 1
                # give a different answer if there was any feedback versus no feedback
                if clue.hasPegs():
                    return True
                else:
                    return False

    def go(self):
        self.environment.generateCode()
        for i in range(2):
            self.makeGuess()
        print("done!")

    def makeGuess(self):
        self.createGuess()
        clue = self.environment.guessCode(self.guess)
        self.clueList.append(clue)
        print("The clue list was " + clue.__str__())
        print("The true code was " + self.environment.getCode().__str__())
