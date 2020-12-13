from Agent import *
from Code import *

"""Chooses a color randomly from a given list.
Used when the agent is testing out a single color."""


def randomColor(viableColors):
    if len(viableColors) > 0:
        color = random.choice(viableColors)
        return color
    else:
        print("The given list is empty and a random color cannot be selected.")


"""Chooses two different colors randomly from a given list"""


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
            print("List is of insufficient length to select two colors.")
            if len(viableColors) == 1:
                color = viableColors[0]
                return color, color
            else:
                return None
    return color1, color2


"""A class that replicates a human strategy of playing through MasterMind."""


class HumanAgent(Agent):
    COLOR_LIST = ["red", "orange", "yellow", "green", "blue", "purple"]
    MAX_GUESSES = 10

    def __init__(self, gameManager):
        # variables to keep track of the game's progress
        self.environment = gameManager
        self.guessList = self.environment.getGuessList()
        self.clueList = self.environment.getClueList()

        # variables relating to the algorithm's guesses
        self.guess = Code([])
        self.nextGuess = Code([])  # a variable that will hold one future guess if the program knows what it will be
        self.futureGuesses = []  # a queue to hold multiple future guesses, in order
        self.guessCount = 0

        # variables keeping track of the use of colors in codes
        self.viableColors = self.COLOR_LIST.copy()
        self.nonviableColors = []  # a list of all of the colors the program knows doesn't appear in the code
        self.usedColors = []  # a list of all of the colors so far used by the program
        self.switchedFirstColor = False  # keeps track of which color is switched out in phase 2

        # variables relating to the first three phases of the game
        self.phaseRound = 1  # changes how the agent plays (from gathering information to acting on that information)
        self.phaseFour = False  # keeps track of whether the program had to enter phase 4 or not
        self.infoGuessList = []  # a list of the three informative guesses made during phases 1-3
        self.infoClueList = []  # a list of their corresponding clues
        # self.bestInfoGuess = Code([])
        self.consistentColor = ""  # a variable to track if a color occurs in all three initial phases

        # variables tracking confirmed progress in guessing the code
        self.testCompleted = False  # whether or not the program has just finished testing two pins
        self.analyzeTest = False  # whether the program is at a point where it should be analyzing the outcome of a test
        self.twoSet = False  # a boolean tracking whether two pin colors and locations have been confirmed
        self.confirmedColors = ["", "", "", ""]
        self.won = False
        self.lost = False

    """Creates the guess that will be used in the next round. This process changes depending on whether the 
    program is gathering info (in one of the first three phases) or interpreting gathered information (after those
    phases are completed). If the former, it will call on makePhaseGuess to calculate what its the guess should 
    be based on the last clue. If in the latter, it will look at the most informative guesses made (those with the 
    most black pins, if any; white pins if not) and use their given clues to make the next move."""

    def createGuess(self):
        # for as long as the game is in one of the first three phases, use makePhaseGuess to create the next guess
        if self.phaseRound:
            newGuess = self.makePhaseGuess()
        else:
            self.guessList = self.environment.getGuessList()
            self.clueList = self.environment.getClueList()
            # first, check to see if the game has been won with the latest guess
            if self.clueList[self.guessCount - 1].getBlackPegs() == 4:
                # if the game has been won, end the program
                self.won = True
                print("Correct guess has been made!")
            if self.testCompleted:
                self.analyzeTest = True
            # next, check to see if the program already knows what its next guess will be
            if len(self.futureGuesses) > 0:
                self.nextGuess = self.futureGuesses.pop([0])
                print("set next guess to be " + self.nextGuess.__str__())
            # if the game knows what its next guess will be, use that guess
            if self.nextGuess is not []:
                if len(self.futureGuesses) == 0:
                    self.testCompleted = True
                newGuess = self.nextGuess
                self.nextGuess = []
            else:
                # if the game just finished testing out two pins, check the result
                if self.analyzeTest:
                    print("Just finished testing two pins.")
                    self.analyzeTest = False
                    self.testCompleted = False
                # a temporary list used to narrow down color choices for a single guess
                clist = self.viableColors.copy()
                # TODO: Define createGuess past this point
                newGuess = Code([])
        # update the guess list
        self.guess = newGuess

    """A process specific to making a guess during one of the first three phases of the game; 
    depending on the phase, the method will use a very simple algorithm to determine what move
    it should make next to gather the most information. In phase one, it will randomly select
    two as of yet unused colors to make a guess with. Once it receives a clue with at least 
    one pin in it, it will move to phase 2. In phase 2, it will choose one of the two colors
    included in the last guess to swap out with a randomly decided new (and unused) color. It
    will then automatically progress to phase 3. In phase 3, the method will choose one of two 
    options: if the last guess made received a clue with at least one pin in it, it will swap 
    out the newest color with a second randomly chosen unused color. If the last guess 
    made received a clue with no pins in it, the method will switch out both colors; it will 
    reinstate the color that had been switched out in phase 2, and replace the other color with 
    a random, new and unused color. If the program needs to enter phase 4, that means the data
    it was given in previous clues misled it on what colors are included in the code. This will
    be helpful to know later on in the analysis process."""

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
        if self.phaseRound == 1:
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
                if self.phaseRound == 2:
                    newGuess.swapPins(0, 2)
                    newGuess.swapPins(1, 3)
                else:
                    if self.phaseRound == 3:
                        newGuess.swapPins(0, 2)
            # choose a new, as of yet unused color to insert into the guess
            newColor = randomColor(clist)
            self.usedColors.append(newColor)
            if self.phaseRound == 2:
                print("Phase 2: Switch out one color randomly")
                if random.randint(0, 1) == 0:
                    newGuess.setPinColor(newColor, 0)
                    newGuess.setPinColor(newColor, 1)
                    self.switchedFirstColor = True
                else:
                    newGuess.setPinColor(newColor, 2)
                    newGuess.setPinColor(newColor, 3)
            else:
                if self.phaseRound == 3:
                    print("Phase 3: Switch out one color depending on previous clue")
                    # if any clue pins were received after the last round...
                    if result:
                        # switch out the newest color with an as of yet unused color
                        if self.switchedFirstColor:
                            oldColor = self.guess.getColors()[1]
                            newGuess.setPinColor(newColor, 0)
                            newGuess.setPinColor(newColor, 1)
                        else:
                            oldColor = self.guess.getColors()[0]
                            newGuess.setPinColor(newColor, 2)
                            newGuess.setPinColor(newColor, 3)
                        self.consistentColor = oldColor
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
                else:
                    if self.phaseRound == 4:
                        print("Phase 4: Misled by data. Return to initially swapped out color.")
                        if self.switchedFirstColor:
                            oldColor = self.guessList[(self.guessCount - 3)].getColors()[0]
                            newGuess = Code([CodePin(oldColor), CodePin(oldColor),
                                             CodePin(newColor), CodePin(newColor)])
                        else:
                            oldColor = self.guessList[(self.guessCount - 3)].getColors()[1]
                            newGuess = Code([CodePin(newColor), CodePin(newColor),
                                             CodePin(oldColor), CodePin(oldColor)])
                        # return to phase 3 in order to move forward in the process
                        self.phaseRound = 3
                        self.phaseFour = True
        return newGuess

    """Used when the program is gathering information. It takes the last clue given and 
    the current phase, and decides what the next course of action will be for makePhaseGuess.
    It will also increment the testRound counter if appropriate, moving the program on to 
    the next phase of gathering information until that step in the process is complete (AKA, 
    it reaches the end of phase 3)."""

    def analyzePhaseClue(self):
        self.guessList = self.environment.getGuessList()
        guess = self.guess
        clue = self.clueList[self.guessCount - 1]
        # check to see if the game has been won; if so, end the method
        if clue.getBlackPegs() == 4:
            self.won = True
            return True
        # if no pins were received, none of the guessed colors are viable
        if not clue.hasPegs():
            for color in self.guess.getColors():
                self.viableColors.remove(color)
        if clue.getBlackPegs() == 3:
            self.handleThreeBlack()
        else:
            # if in phase 1...
            if self.phaseRound == 1:
                # if the guess got any feedback, move to phase 2
                if clue.hasPegs():
                    self.phaseRound += 1
                return True
            # if in phase 2...
            else:
                if self.phaseRound == 2:
                    # automatically move to phase 3
                    self.phaseRound += 1
                    # return a different result based on whether any clue pins were given
                    if clue.hasPegs():
                        return True
                    return False
                else:
                    if self.phaseRound == 3:
                        if clue.hasPegs():
                            # finish the third phase and move on to the next stage of the game
                            # populate the lists of informative guesses and clues
                            # (these are the last three guesses made before the end of the three phases)
                            if not self.phaseFour:
                                for i in range(3):
                                    self.infoGuessList.append(self.guessList[self.guessCount - (i + 1)])
                                    self.infoClueList.append(self.clueList[self.guessCount - (i + 1)])
                            else:
                                # the program had to reverse course based on misleading data
                                for i in range(4):
                                    # skip the guess that received no white or black pegs
                                    if i != 1:
                                        self.infoGuessList.append(self.guessList[self.guessCount - (i + 1)])
                                        self.infoClueList.append(self.clueList[self.guessCount - (i + 1)])
                            self.infoGuessList.reverse()
                            self.infoClueList.reverse()
                            # end the test rounds and reset the list of used colors
                            self.phaseRound = 0
                            self.usedColors = []
                            self.analyzeFirstPhases()
                        else:
                            # move on to the (uncommon) fourth phase
                            self.phaseRound += 1

    """Takes the information gained from the first three phases of the game and
    uses it to determine what route it should take next."""

    def analyzeFirstPhases(self):
        blackPegsList = []
        whitePegsList = []
        for clue in self.infoClueList:
            blackPegs = clue.getBlackPegs()
            whitePegs = clue.getWhitePegs()
            # print("blackPegs: " + str(blackPegs) + ", whitePegs: " + str(whitePegs))
            blackPegsList.append(blackPegs)
            whitePegsList.append(whitePegs)
        minBlackPegs = 4  # a local variable to track the minimum number of black pegs across all phases
        maxBlackPegs = 0  # to track the maximum number of black pegs
        minWhitePegs = 4
        maxWhitePegs = 0
        for pegs in blackPegsList:
            if pegs < minBlackPegs:
                minBlackPegs = pegs
            if pegs > maxBlackPegs:
                maxBlackPegs = pegs
        for pegs in whitePegsList:
            if pegs < minWhitePegs:
                minWhitePegs = pegs
            if pegs > maxWhitePegs:
                maxWhitePegs = pegs
        print("Minimum number of black pegs: " + str(minBlackPegs))
        print("Minimum number of white pegs: " + str(minWhitePegs))
        if self.consistentColor != "" and not self.phaseFour:
            print(str(self.consistentColor) + " appeared 3 times.")
            # as one color appeared in all three guesses, and no other color appeared more
            # than once, the minimum number of black pegs applies to the reoccurring color

            # a near-win condition has been found
            if maxBlackPegs == 3:
                print("Max black pegs: 3")
                # access the guess that received three black pins
                count = 0
                for pegs in blackPegsList:
                    if pegs == 3:
                        self.guess = self.infoGuessList[count]
                    count += 1
                # finish the game by testing out which pin does not belong and swapping out colors for it
                self.handleThreeBlack()
            if maxWhitePegs == 3:
                print("Max white pegs: 3")
                # access the guess that received three white pins
                count = 0
                for pegs in whitePegsList:
                    if pegs == 3:
                        self.guess = self.infoGuessList[count]
                    count += 1
                # swap around the pins
                self.guess.swapPins(0, 2)
                self.guess.swapPins(1, 3)
                self.handleThreeBlack()
            else:
                # the two consistent pins are in the correct position
                if minBlackPegs == 2:  # minBlackPegs has a maximum value of 2 and a minimum value of 0 in this case
                    print("Min black pegs: 2")
                    if self.switchedFirstColor:
                        self.setAsConfirmed(self.consistentColor, 2)
                        self.setAsConfirmed(self.consistentColor, 3)
                    else:
                        self.setAsConfirmed(self.consistentColor, 0)
                        self.setAsConfirmed(self.consistentColor, 1)
                    self.twoSet = True  # two pins have been confirmed to be in the correct locations
                # the two consistent pins are in the code, but in the wrong position
                if minWhitePegs == 2:
                    print("Min white pegs: 2")
                    if self.switchedFirstColor:
                        self.setAsConfirmed(self.consistentColor, 0)
                        self.setAsConfirmed(self.consistentColor, 1)
                    else:
                        self.setAsConfirmed(self.consistentColor, 2)
                        self.setAsConfirmed(self.consistentColor, 3)
                    self.twoSet = True
                # one of the consistent pins is in the correct position
                if minBlackPegs == 1:
                    print("Min black pegs: 1")
                    # test out which pin is in the correct position
                    if self.switchedFirstColor:
                        self.test(2, 3)
                    else:
                        self.test(0, 1)
                if minWhitePegs == 1:
                    print("Min white pegs: 1")
                    # test out which pin would be in the correct position
                    self.guess.swapPins(0, 2)
                    self.guess.swapPins(1, 3)
                    if self.switchedFirstColor:
                        self.test(0, 1)
                    else:
                        self.test(2, 3)
                if self.won:
                    return
                else:
                    if maxBlackPegs == 2:
                        # TODO: handle two black pegs
                        pass

    """Takes a color and index and sets that index in the code as confirmed to be the given color."""

    def setAsConfirmed(self, color, location):
        print("Setting pin at index " + str(location) + " as confirmed to be " + color + ".")
        if 0 <= location <= 3:
            if color in COLOR_LIST:
                self.confirmedColors[location] = color
            else:
                print("Given color is not a known pin color.")
        else:
            print("Given index is not within acceptable range (0-3).")

    """Confirms the pin at the given index to be its color."""

    def setPinAsConfirmed(self, location):
        color = self.guess.getPin(location).color
        self.setAsConfirmed(color, location)

    """Takes two positions in the guess and returns which of the two pins is in the correct location."""

    def test(self, position1, position2):
        print("Testing pins at " + str(position1) + " and " + str(position2))
        color = self.guess.getPin(position1).color
        self.guess.setPinColor("", position1)
        clue = self.makeGuess(self.guess)
        if self.won:
            return
        # find the original guess's corresponding clue to compare with
        oldPegs = self.clueList[self.guessCount - 2].getBlackPegs()
        print("Old pegs: " + str(oldPegs))
        print("New pegs: " + str(clue.getBlackPegs()))
        # if the new clue has as many black pegs as the old clue...
        if clue.getBlackPegs() >= oldPegs:
            # this means that the pin that had NOT been tested is in the correct position
            self.setPinAsConfirmed(position2)
        # if not, this means that the pin that HAD been tested had already been in the correct position
        else:
            self.setAsConfirmed(color, position1)

    """Tests the full code to find out which pins are in the correct locations. Used when the latest code received
    included three black pins."""

    def handleThreeBlack(self):
        print("Handling three black pins...")
        guess = self.guess.copy()
        color1 = guess.getPin(0).color
        color2 = guess.getPin(1).color
        guess.swapPins(0, 1)
        clue = self.makeGuess(guess)
        if clue.getBlackPegs() >= 2:
            self.setPinAsConfirmed(2)
            self.setPinAsConfirmed(3)
            self.test(0, 1)
            index = self.availablePositions()[0]
            print("Unknown: " + str(index))
        else:
            self.setAsConfirmed(color1, 0)
            self.setAsConfirmed(color2, 0)
            self.test(2, 3)
            index = self.availablePositions()[0]
            print("Unknown: " + str(index))

    """Handles any situation where the most recent guess made had two pins set in the correct location."""

    def handleTwoUnknowns(self, position1, position2):
        pass

    """Handles any situation where there is only one incorrect pin, and its location is known."""

    def handleOneUnknown(self, position):
        clist = self.viableColors.copy()
        # remove as an option any colors that have been guessed and proven incorrect
        for guess in self.guessList:
            sameCode = True
            for i in range(4):
                if i != position:
                    if guess.getPin(i).color != self.guess.getPin(i).color:
                        sameCode = False
            if sameCode:
                clist.remove(guess.getPin(position).color)
        for color in clist:
            if not self.won:
                self.guess.setPinColor(color, position)
                self.makeGuess(self.guess)
        print("***Correct guess has been made!***")
        return True

    # TODO: May be able to remove this method
    """Returns a list of all of the guesses that belonged to the most recent test."""

    def getTestGuesses(self):
        self.guessList = self.environment.getGuessList()
        testList = []
        for guess in self.guessList:
            if guess.checkIfTest():
                testList.append(guess)
                guess.removeAsTest()
        return testList

    """Returns which positions (indices) in the code have not been confirmed yet."""

    def availablePositions(self):
        indexList = []
        count = 0
        for item in self.confirmedColors:
            if item == "":
                indexList.append(count)
            count += 1
        return indexList

    """"Calls the game manager to figure out the corresponding code for the given guess"""

    def makeGuess(self, guess=None):
        if self.guessCount > self.MAX_GUESSES:
            print("---Ran out of guesses! Following guesses exceed maximum amount allowed---")
        # make sure that all confirmed colors are set correctly
        for i in range(4):
            if self.confirmedColors[i] != "":
                self.guess.setPinColor(self.confirmedColors[i], i)
        print("The AGENT'S GUESS is: " + self.guess.__str__())
        print("The TRUE CODE is " + self.environment.getCode().__str__())
        if guess is not None:
            clue = self.environment.guessCode(guess)
        else:
            clue = self.environment.guessCode(self.guess)
        if clue.getBlackPegs() == 4:
            print("Correct guess has been made!")
            self.won = True
            return clue
        self.guessCount += 1
        print("The clue given was " + clue.__str__())
        print("Confirmed pins..." + str(self.confirmedColors))
        print("--------------------------")
        return clue

    """Runs through the game until the maximum number of guesses has been met or
    the correct code has been guessed."""

    def go(self):
        self.environment.generateCode()
        for i in range(5):
            self.createGuess()
            self.makeGuess()
        print("Done!")
