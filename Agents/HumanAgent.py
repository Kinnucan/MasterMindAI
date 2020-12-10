import random
from Agent import *
from GameManager import *
from CodePin import *
from Code import *


# choose a color randomly from a given list
# used when the agent is testing out a single color
def randomColor(viableColors):
    if len(viableColors) > 0:
        color = random.choice(viableColors)
        return color
    else:
        print("The given list is empty and a random color cannot be selected")


# choose two different colors randomly from a given list
def randomTwoColors(viableColors):
    if len(viableColors) > 2:
        clist = viableColors.copy()
        color1 = randomColor(clist)
        clist.remove(color1)
        color2 = randomColor(clist)
    else:
        if len(viableColors) == 2:
            color1 = viableColors[0]
            color2 = viableColors[1]
        else:
            print("List is of insufficient length to select two colors")
            if len(viableColors) == 1:
                color = viableColors[0]
                return color, color
            else:
                return None
    return color1, color2


"""A class that replicates a human strategy of playing through MasterMind."""


class HumanAgent(Agent):
    COLOR_LIST = ["red", "orange", "yellow", "green", "blue", "purple"]
    #COLOR_LIST = ["blue", "purple"]


    def __init__(self, gameManager):
        self.environment = gameManager
        self.guessList = self.environment.getGuessList()
        self.clueList = self.environment.getClueList()
        self.guess = Code([])
        self.guessCount = 0
        self.viableColors = self.COLOR_LIST.copy()
        self.usedColors = []
        self.testRound = 1  # changes how the agent plays (from gathering information to acting on that information)
        self.switchedFirstColor = False # keeps track of which color is switched out in phase 2
        self.infoGuessList = [] # a list of the three informative guesses made during phases 1-3
        self.infoClueList = [] # a list of their corresponding clues
        self.bestInfoGuess = Code([])
        self.won = False

    def createGuess(self):
        if self.testRound:
            newGuess = self.makePhaseGuess()
        else:
            self.guessList = self.environment.getGuessList()
            # a temporary list used to narrow down color choices for a single guess
            clist = self.viableColors.copy()
            # check to see if the game has been won with the latest guess
            if self.clueList[self.guessCount-1].getBlackPegs() == 4:
                # if the game has been won, end the program
                self.won = True
                print("Correct guess has been made!")
                pass
            newGuess = []
        # update the guess list
        self.guess = newGuess
        self.guessCount += 1
        print("The agent's guess is: " + self.guess.__str__())

    def makePhaseGuess(self):
        self.guessList = self.environment.getGuessList()
        # a temporary list used to narrow down color choices for a single guess
        # analyze the most recent clue, if there is one (empty clues count)
        if self.guessCount > 0:
            result = self.analyzePhaseClue()
        clist = self.viableColors.copy()
        if self.won:
            print("Correct guess has been made!")
            pass
        if self.testRound == 1:
            print("Phase 1: Two random unused colors")
            color1, color2 = randomTwoColors(clist)
            self.usedColors.append(color1)
            self.usedColors.append(color2)
            newGuess = Code([CodePin(color1), CodePin(color1), CodePin(color2), CodePin(color2)])
        # second phase: switch out one color to see how it affects the given clue
        else:
            newGuess = self.guess.copy()
            # create a temporary list of acceptable colors
            if len(clist) > 2:
                clist = self.guess.getViableUnused(clist)
                for color in self.usedColors:
                    if color in clist:
                        clist.remove(color)
            else:
                if self.testRound == 2:
                    newGuess.swapPins(0, 2)
                    newGuess.swapPins(1, 3)
                else:
                    if self.testRound == 3:
                        newGuess.swapPins(0, 2)
            # choose a new, as of yet unused color to insert into the guess
            newColor = randomColor(clist)
            self.usedColors.append(newColor)
            if self.testRound == 2:
                print("Phase 2: Switch out one color randomly")
                if random.randint(0, 1) == 0:
                    newGuess.setPinColor(newColor, 0)
                    newGuess.setPinColor(newColor, 1)
                    self.switchedFirstColor = True
                else:
                    newGuess.setPinColor(newColor, 2)
                    newGuess.setPinColor(newColor, 3)
            else:
                if self.testRound == 3:
                    print("Phase 3: Switch out one color depending on previous clue")
                    # if any clue pins were received after the last round...
                    if result:
                        # switch out the newest color with an as of yet unused color
                        if self.switchedFirstColor:
                            newGuess.setPinColor(newColor, 0)
                            newGuess.setPinColor(newColor, 1)
                        else:
                            newGuess.setPinColor(newColor, 2)
                            newGuess.setPinColor(newColor, 3)
                    # if not...
                    else:
                        # reinstate the color that had been switched out
                        if self.switchedFirstColor:
                            oldColor = self.guessList[(self.guessCount - 2)].getColors()[0]
                            newGuess = Code([CodePin(oldColor), CodePin(oldColor),
                                             CodePin(newColor), CodePin(newColor)])
                        else:
                            oldColor = self.guessList[(self.guessCount - 2)].getColors()[1]
                            newGuess = Code([CodePin(newColor), CodePin(newColor),
                                             CodePin(oldColor), CodePin(oldColor)])
                    self.testRound = 0
        return newGuess

    def analyzePhaseClue(self):
        self.guessList = self.environment.getGuessList()
        guess = self.guess
        clue = self.clueList[self.guessCount-1]
        # check to see if the game has been won; if so, end the method
        if clue.getBlackPegs() == 4:
            self.won = True
            return True
        # if in phase 1...
        if self.testRound == 1:
            # if the guess got any feedback, move to phase 2
            if clue.hasPegs():
                self.testRound += 1
            # if no clue was given, neither color is present in the hidden code
            # both can be removed from the list of viable colors
            else:
                for color in self.guess.getColors():
                    self.viableColors.remove(color)
            return True
        # if in phase 2...
        else:
            if self.testRound == 2:
                # automatically move to phase 3
                self.testRound += 1
                # return a different result based on whether any clue pins were given
                if clue.hasPegs():
                    return True
                for color in self.guess.getColors():
                    self.viableColors.remove(color)
                return False
            else:
                if self.testRound == 3:
                    # finish the third phase and move on to the next stage of the game
                    # populate the lists of informative guesses and clues
                    # (these are the last three guesses made before the end of the three phases)
                    for i in range(3):
                        self.infoGuessList.append(self.guessList[self.guessCount - (i + 1)])
                        self.infoClueList.append(self.clueList[self.guessCount - (i + 1)])
                    self.analyzeFirstPhases()

    def analyzeFirstPhases(self):
        newGuess = Code([])
        for clue in self.infoClueList:
            index = self.infoClueList.index(clue)
            blackPegs = clue.getBlackPegs()
            if blackPegs == 3:
                guess = self.infoGuessList[index]


    def go(self):
        self.environment.generateCode()
        for i in range(5):
            self.makeGuess()
        print("Done!")

    def makeGuess(self):
        print("The true code is " + self.environment.getCode().__str__())
        self.createGuess()
        clue = self.environment.guessCode(self.guess)
        print("The clue given was " + clue.__str__())
        print("--------------------------")
