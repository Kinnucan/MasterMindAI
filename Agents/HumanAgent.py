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
        self.guess = Code([])
        self.guessCount = 0
        self.viableColors = self.COLOR_LIST.copy()
        self.testRound = 1  # changes how the agent plays (from gathering information to acting on that information)
        self.switchedFirstColor = False # keeps track of which color is switched out in phase 2
        self.won = False

    def createGuess(self):
        self.guessList = self.environment.getGuessList()
        # analyze the most recent clue, if there is one (empty clues count)
        if self.guessCount > 0:
            result = self.analyzeLatestClue()
        # if the game has been won, end the program
        if self.won:
            print("Correct guess has been made!")
        # a temporary list used to narrow down color choices for a single guess
        clist = self.viableColors.copy()
        # first phase: keep guessing until you receive at least one clue in return
        if self.testRound:
            if self.testRound == 1:
                print("Phase 1: Two random unused colors")
                color1, color2 = randomTwoColors(clist)
                newGuess = Code([CodePin(color1), CodePin(color1), CodePin(color2), CodePin(color2)])
            # second phase: switch out one color to see how it affects the given clue
            else:
                prevColors = self.guess.getColors()
                # choose one of the previous colors to reuse, and replace the other color with the new selection
                prevColor1 = prevColors[0]
                prevColor2 = prevColors[1]
                # create a temporary list of acceptable colors
                clist = self.guess.getViableUnused(clist)
                # choose a new, as of yet unused color to insert into the guess
                newColor = randomColor(clist)
                if self.testRound == 2:
                    print("Phase 2: Switch out one color randomly")
                    if random.randint(0, 1) == 0:
                        newGuess = Code([CodePin(prevColor1), CodePin(prevColor1),
                                         CodePin(newColor), CodePin(newColor)])
                    else:
                        newGuess = Code([CodePin(newColor), CodePin(newColor),
                                         CodePin(prevColor2), CodePin(prevColor2)])
                        self.switchedFirstColor = True
                else:
                    if self.testRound == 3:
                        print("Phase 3: Switch out one color depending on previous clue")
                        # if any clue pins were received after the last round...
                        if result:
                            # switch out the newest color with an as of yet unused color
                            if self.switchedFirstColor:
                                newGuess = Code([CodePin(newColor), CodePin(newColor),
                                                 CodePin(prevColor2), CodePin(prevColor2)])
                            else:
                                newGuess = Code([CodePin(prevColor1), CodePin(prevColor1),
                                                 CodePin(newColor), CodePin(newColor)])
                        # if not...
                        else:
                            # reinstate the color that had been switched out
                            if self.switchedFirstColor:
                                oldColor = self.guessList[self.guessCount-1].getColors()[0]
                                newGuess = Code([CodePin(oldColor), CodePin(oldColor),
                                                 CodePin(newColor), CodePin(newColor)])
                            else:
                                oldColor = self.guessList[self.guessCount - 1].getColors()[1]
                                newGuess = Code([CodePin(newColor), CodePin(newColor),
                                                 CodePin(oldColor), CodePin(oldColor)])
        else:
            pass
        # update the guess list
        self.guessList.append(newGuess)
        self.guess = newGuess
        self.guessCount += 1
        print("The agent's guess is: " + self.guess.__str__())

    def analyzeLatestClue(self):
        guess = self.guess
        clue = self.clueList[self.guessCount]
        print("Clue being analyzed for this round: " + clue.__str__())
        # check to see if the game has been won; if so, end the method
        if clue.getBlackPegs() == 4:
            self.won = True
            return True
        # if in phase 1...
        if self.testRound == 1:
            # if the guess got any feedback, move to phase 2
            if clue.hasPegs():
                print("FIRST CLUE given! Moving to phase 2")
                self.testRound += 1
            # if no clue was given, neither color is present in the hidden code
            # both can be removed from the list of viable colors
            else:
                for color in self.guess.getColors():
                    print("Removing " + color + " from color list")
                    self.viableColors.remove(color)
            return True
        # if in phase 2...
        else:
            if self.testRound == 2:
                # automatically move to phase 3
                self.testRound += 1
                # return a different result based on whether any clue pins were given
                if clue.hasPegs():
                    print("Clue received in second phase HAS PEGS")
                    return True
                print("Clue received in second phase DOES NOT HAVE PEGS")
                for color in self.guess.getColors():
                    self.viableColors.remove(color)
                return False
            else:
                if self.testRound == 3:
                    # finish the third phase and move on to the next stage of the game
                    print("Got to round 3")

    def go(self):
        self.environment.generateCode()
        for i in range(3):
            self.makeGuess()
        print("Done!")

    def makeGuess(self):
        print("The true code is " + self.environment.getCode().__str__())
        self.createGuess()
        clue = self.environment.guessCode(self.guess)
        self.clueList.append(clue)
        print("The clue given was " + clue.__str__())
        print("--------------------------")

    def swapPins(self, firstPosition, secondPosition):
        newGuess = self.guess
        pin1 = newGuess.getPin(firstPosition)
        pin2 = newGuess.getPin(secondPosition)
        newGuess.setPin(pin1, secondPosition)
        newGuess.setPin(pin2, secondPosition)
