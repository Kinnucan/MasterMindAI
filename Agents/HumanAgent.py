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
                color1 = ""
                color2 = ""
    return color1, color2


"""A class that replicates a human strategy of playing through MasterMind."""


class HumanAgent(Agent):
    COLOR_LIST = ["red", "orange", "yellow", "green", "blue", "purple"]
    MAX_GUESSES = 20

    def __init__(self, gameManager):
        # variables to keep track of the game's progress
        self.environment = gameManager
        self.guessList = self.environment.getGuessList()
        self.clueList = self.environment.getClueList()

        # variables relating to the algorithm's guesses
        self.guess = Code([])
        self.nextGuess = Code([])  # a variable that will hold one future guess if the program knows what it will be
        # self.futureGuesses = []  # a queue to hold multiple future guesses, in order
        self.guessCount = 0

        # variables keeping track of the use of colors in codes
        self.viableColors = self.COLOR_LIST.copy()
        self.nonviableColors = []  # a list of all of the colors the program knows doesn't appear in the code
        self.usedColors = []  # a list of all of the colors so far used by the program
        self.switchedFirstColor = False  # keeps track of which color is switched out in phase 2

        # variables relating to the first three phases of the game
        self.phaseRound = 1  # changes how the agent plays (from gathering information to acting on that information)
        self.switchedBack = False  # keeps track of whether the code received any clue pins in phase
        self.enteredPhaseFour = False  # keeps track of whether the program had to enter phase 4 or not
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
        newGuess = Code([])
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
            print("The game has been won!")
            return
        if self.lost:
            print("The game has been lost.")
            return
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
                            limit = len(self.guess.getColors()) - 1
                            oldColor = self.guess.getColors()[limit]
                            newGuess.setPinColor(newColor, 0)
                            newGuess.setPinColor(newColor, 1)
                        else:
                            oldColor = self.guess.getColors()[0]
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
                            limit = len(self.guessList[(self.guessCount - 2)].getColors()) - 1
                            oldColor = self.guessList[(self.guessCount - 2)].getColors()[limit]
                            newGuess = Code([CodePin(newColor), CodePin(newColor),
                                             CodePin(oldColor), CodePin(oldColor)])
                        # note that the program had to switch back to the old color
                        self.switchedBack = True
                    self.consistentColor = oldColor
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
                        self.enteredPhaseFour = True
                        self.switchedBack = True
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
            return
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
                return
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
                            if not self.enteredPhaseFour:
                                if not self.switchedBack:
                                    for i in range(3):
                                        self.infoGuessList.append(self.guessList[self.guessCount - (i + 1)])
                                        self.infoClueList.append(self.clueList[self.guessCount - (i + 1)])
                                else:
                                    # ignore the second guess and its clue if no pins were received in phase 2
                                    for i in range(3):
                                        if i != 1:
                                            self.infoGuessList.append(self.guessList[self.guessCount - (i + 1)])
                                            self.infoClueList.append(self.clueList[self.guessCount - (i + 1)])
                            else:
                                # the program had to reverse course based on misleading data
                                for i in range(4):
                                    # skip the middle guesses
                                    if i != 1 and i != 2:
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
        # ignore the second guess and its clue if no pins were received during phase 2
        if self.switchedBack:
            self.infoClueList.pop(1)
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
        # as one color appeared in all guesses in self.infoGuessList, and no other color appeared more
        # than once, the minimum number of black pegs applies to the reoccurring color

        # a near-win condition has been found
        if maxWhitePegs == 4:
            print("Max white pegs: 4")
            self.guess = self.findInfoGuessByPegs(whitePegsList, 4)
            self.guess.swapPins(0, 2)
            self.guess.swapPins(1, 3)
            self.makeGuess(self.guess)
            return
        if maxBlackPegs == 3:
            print("Max black pegs: 3")
            # access the guess that received three black pins
            self.guess = self.findInfoGuessByPegs(blackPegsList, 3)
            # finish the game by testing out which pin does not belong and swapping out colors for it
            self.handleThreeBlack()
            return
        if maxWhitePegs == 3:
            print("Max white pegs: 3")
            # access the guess that received three white pins
            self.guess = self.findInfoGuessByPegs(whitePegsList, 3)
            # swap around the pins
            self.guess.swapPins(0, 2)
            self.guess.swapPins(1, 3)
            self.handleThreeBlack(True)
            return
        else:
            # the two consistent pins are in the correct position
            if minBlackPegs == 2:  # minBlackPegs has a maximum value of 2 and a minimum value of 0 in this case
                print("Min black pegs: 2")
                if (self.switchedFirstColor and not self.switchedBack) or \
                    (self.switchedBack and not self.switchedFirstColor):
                    self.setAsConfirmed(self.consistentColor, 2)
                    self.setAsConfirmed(self.consistentColor, 3)
                    self.handleTwoUnknowns()
                    return
                else:
                    self.setAsConfirmed(self.consistentColor, 0)
                    self.setAsConfirmed(self.consistentColor, 1)
                    self.handleTwoUnknowns()
                    return
            # the two consistent pins are in the code, but in the wrong position
            if minWhitePegs == 2:
                print("Min white pegs: 2")
                if (self.switchedFirstColor and not self.switchedBack) or \
                    (self.switchedBack and not self.switchedFirstColor):
                    self.setAsConfirmed(self.consistentColor, 0)
                    self.setAsConfirmed(self.consistentColor, 1)
                    self.handleTwoUnknowns()
                    return
                else:
                    self.setAsConfirmed(self.consistentColor, 2)
                    self.setAsConfirmed(self.consistentColor, 3)
                    self.handleTwoUnknowns()
                    return
            # one of the consistent pins is in the correct position
            if minBlackPegs == 1:
                print("Min black pegs: 1")
                # test out which pin is in the correct position
                self.guess = self.findInfoGuessByPegs(blackPegsList, 1)
                if (self.switchedFirstColor and not self.switchedBack) or \
                    (self.switchedBack and not self.switchedFirstColor):
                    self.test(2, 3, False, self.guess)
                else:
                    self.test(0, 1, False, self.guess)
                if self.won:
                    return
                if minWhitePegs < 1:
                    self.finalAnalysis()
                    return
            # one of the consistent pins is the correct color, but in the wrong position
            if minWhitePegs == 1:
                print("Min white pegs: 1")
                # test out which pin would be in the correct position
                self.guess = self.findInfoGuessByPegs(whitePegsList, 1)
                oldGuess = self.guess
                self.guess.swapPins(0, 2)
                self.guess.swapPins(1, 3)
                if (self.switchedFirstColor and not self.switchedBack) or \
                   (self.switchedBack and not self.switchedFirstColor):
                    self.test(0, 1, True, oldGuess)
                else:
                    self.test(2, 3, True, oldGuess)
                if self.won or self.lost:
                    return
                self.finalAnalysis()
                return
            else:
                # as the minimum number of black and white pegs was 0, these pegs apply to a swapped out color
                # these steps will not be reached if switchedBack is true
                if maxBlackPegs == 2:
                    print("Max black pegs: 2")
                    self.guess = self.findInfoGuessByPegs(blackPegsList, 2)
                    if self.switchedFirstColor:
                        self.setAsConfirmed(self.guess.getPin(0).color, 0)
                        self.setAsConfirmed(self.guess.getPin(1).color, 1)
                        self.handleTwoUnknowns()
                        return
                    else:
                        self.setAsConfirmed(self.guess.getPin(2).color, 2)
                        self.setAsConfirmed(self.guess.getPin(3).color, 3)
                        self.handleTwoUnknowns()
                        return
                else:
                    # same here: these white pegs must apply to a swapped out color by process of elimination
                    if maxWhitePegs == 2:
                        print("Max white pegs: 2")
                        self.guess = self.findInfoGuessByPegs(whitePegsList, 2)
                        if self.switchedFirstColor:
                            self.setAsConfirmed(self.guess.getPin(0).color, 2)
                            self.setAsConfirmed(self.guess.getPin(1).color, 3)
                            self.handleTwoUnknowns()
                            return
                        else:
                            self.setAsConfirmed(self.guess.getPin(2).color, 0)
                            self.setAsConfirmed(self.guess.getPin(3).color, 1)
                            self.handleTwoUnknowns()
                            return
                    else:
                        # there will either be two clues with one black peg, or two clues with one white peg
                        # now we will figure out which is which (or if both are true)
                        print("Looking at worst-case scenario...")
                        colorList = []
                        count = 0
                        for pegs in blackPegsList:
                            if pegs == 1:
                                if self.switchedFirstColor:
                                    colorList.append(self.infoGuessList[count].getPin(0).color)
                                else:
                                    colorList.append(self.infoGuessList[count].getPin(2).color)
                            count += 1
                        if len(colorList) == 1:
                            self.guess = self.findInfoGuessByPegs(blackPegsList, 1)
                            if self.switchedFirstColor:
                                self.test(0, 1, False, self.guess)
                            else:
                                self.test(2, 3, False, self.guess)
                            self.finalAnalysis()
                            return
                        else:
                            noBlackPegs = self.findInfoGuessByPegs(blackPegsList, 0)
                            count = 0
                            for guess in self.infoGuessList:
                                clue = self.infoClueList[count]
                                if guess != noBlackPegs:
                                    print(guess.__str__() + " is not equal to " + noBlackPegs.__str__())
                                    if self.switchedFirstColor:
                                        self.guess = guess
                                        self.test(0, 1, False, guess)
                                    else:
                                        self.guess = guess
                                        self.test(2, 3, False, guess)
                            self.handleTwoUnknowns()
                            return

    """Finishes up the game if it hasn't been finished already. This method is called when one pin location has been
    determined, and it uses information from the first three phases of the game to find the location of a second pin
    and begin wrapping up the guessing process from there."""

    def finalAnalysis(self):
        print("Entering final analysis stage.")
        unconfirmed = self.getUnconfirmedPositions()
        # reroute finalAnalysis in case there are less than three unknown pins in the code
        if len(unconfirmed) == 2:
            self.handleTwoUnknowns()
            return
        if len(unconfirmed) == 1:
            self.handleOneUnknown()
            return
        # handle three unknowns
        confirmedPos = self.getConfirmedPositions()[0]
        # a list of the two positions that will be assigned color1 as a color
        posList = []
        receivedPegs = False
        while not receivedPegs:
            posList = []
            # take two random colors; one will be put in two available positions, one in one available position
            color1, color2 = randomTwoColors(self.viableColors)
            print("Testing " + color1 + " and " + color2 + " as colors.")
            for i in range(4):
                if i != confirmedPos:
                    self.guess.setPinColor(color1, i)
            # set the remaining color to be either in the last position or second-to-last position
            if confirmedPos != 3:
                self.guess.setPinColor(color2, 3)
                # denote positions for color1
                for i in range(3):
                    if i != confirmedPos:
                        posList.append(i)
            else:
                self.guess.setPinColor(color2, 2)
                # the positions of color1 are confirmed to be at 0 and 1 in this situation
                posList.append(0)
                posList.append(1)
            print("Pos list: " + str(posList))
            clue = self.makeGuess(self.guess)
            if self.lost or self.won:
                return
            wp = clue.getWhitePegs()
            bp = clue.getBlackPegs()
            # if any pegs were received in response to the new colors...
            if wp != 0 or bp > 1:
                receivedPegs = True
                print("Pegs received. Moving on.")
            # if not, remove them as guessing options from now
            else:
                self.viableColors.remove(color1)
                self.viableColors.remove(color2)
        # this means that two of the new colors are in the right place
        if clue.getBlackPegs() == 3:
            print("Three black pegs in final analysis.")
            self.handleThreeBlack()
            return
        else:
            # this means that one of the new colors is in the right place.
            # swap out the color2 slot with a new color. If that pin had been
            # in the correct location, the resulting clue will have
            # just one black peg. If not, test both color1 slots against
            # one another.
            if clue.getBlackPegs() == 2:
                print("Two black pegs in final analysis.")
                if confirmedPos != 3:
                    color = self.guess.getPin(3).color
                    self.guess.setPinColor("", 3)
                else:
                    color = self.guess.getPin(2).color
                    self.guess.setPinColor("", 2)
                # reassign clue
                clue = self.makeGuess(self.guess)
                if self.lost or self.won:
                    return
                # return the pin to its previous color
                if confirmedPos != 3:
                    self.guess.setPinColor(color, 3)
                else:
                    self.guess.setPinColor(color, 2)
                if clue.getBlackPegs() == 1:
                    print("Got back one black peg.")
                    if confirmedPos == 3:
                        self.setAsConfirmed(color2, 2)
                    else:
                        self.setAsConfirmed(color2, 3)
                    self.handleTwoUnknowns()
                    return
                else:
                    print("Got back two black pegs.")
                    self.test(posList[0], posList[1])
                    self.handleTwoUnknowns()
                    return
            else:
                # this means that both added colors are in the code:
                # move color1 into the color2 slot, move color2 into both color1 slots,
                # and then test which one is in the right location and call
                # handleOneUnknown afterwards.
                if clue.getWhitePegs() == 2:
                    print("Two white pegs in final analysis.")
                    # set the color2 slot as confirmed to be color1
                    if confirmedPos == 3:
                        self.setAsConfirmed(color1, 2)
                    else:
                        self.setAsConfirmed(color1, 3)
                    self.guess.setPinColor(color2, posList[0])
                    self.guess.setPinColor(color2, posList[1])
                    self.test(posList[0], posList[1])
                    self.handleOneUnknown()
                    pass
                # this means that one added color is in the code:
                # move color1 into the color2 slot and make a guess.
                # if that receives 0 white pegs, move color2 into both
                # color1 slots and test which one is the right slot for
                # color2. Then call handleTwoUnknowns afterwards.
                if clue.getWhitePegs() == 1:
                    print("One white peg in final analysis.")
                    # switch the color2 slot to be color1
                    if confirmedPos == 3:
                        self.guess.setPinColor(color1, 2)
                    else:
                        self.guess.setPinColor(color1, 3)
                    clue = self.makeGuess(self.guess)
                    if self.lost or self.won:
                        return
                    if clue.getBlackPegs() == 2:
                        if confirmedPos == 3:
                            self.setPinAsConfirmed(2)
                        else:
                            self.setPinAsConfirmed(3)
                        self.handleTwoUnknowns()
                        return
                    else:
                        if clue.getWhitePegs() == 1:
                            self.test(posList[0], posList[1])
                            self.handleTwoUnknowns()
                            return
                        else:
                            # it should receive 0 white pegs otherwise
                            self.guess.setPinColor(color2, posList[0])
                            self.guess.setPinColor(color2, posList[1])
                            self.test(posList[0], posList[1])
                            self.handleTwoUnknowns()
                            return


    def reduceViableColors(self):
        # use this space to reduce viableColors by:
        # looking at what codes have no black pins
        # looking at what codes have no white pins
        # finding any common colors between them
        # checking to make sure the color has not been moved
        # removing the color from self.viableColors
        pass

    def findInfoGuessByPegs(self, pegsList, pegNum):
        newGuess = Clue([])
        count = 0
        for pegs in pegsList:
            if pegs == pegNum:
                newGuess = self.infoGuessList[count]
            count += 1
        print("Guess with " + str(pegNum) + " peg(s) found: " + newGuess.__str__())
        return newGuess

    def findClueByGuess(self, guess):
        self.guessList = self.environment.getGuessList()
        self.clueList = self.environment.getClueList()
        clue = []
        count = 0
        for item in self.guessList:
            if item == guess:
                clue = self.clueList[count]
            count += 1
        if not clue:
            print("Given guess does not exist in records.")
        return clue

    """Takes a color and index and sets that index in the code as confirmed to be the given color."""

    def setAsConfirmed(self, color, location):
        print("Setting pin at index " + str(location) + " as confirmed to be " + color + ".")
        if 0 <= location <= 3:
            if color in COLOR_LIST:
                self.guess.setPinColor(color, location)
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

    def test(self, position1, position2, checkWhitePegs=False, oldGuess=None):
        if oldGuess is None:
            oldGuess = self.guess
        print("Testing pins at " + str(position1) + " and " + str(position2) + " in guess " + oldGuess.__str__())
        print("Checking against " + oldGuess.__str__())
        oldClue = self.findClueByGuess(oldGuess)
        # store the pegs that the new clue will be compared to
        if checkWhitePegs:
            oldPegs = oldClue.getWhitePegs()
        else:
            oldPegs = oldClue.getBlackPegs()
        color = self.guess.getPin(position1).color
        self.guess.setPinColor("", position1)
        clue = self.makeGuess(self.guess, True)
        if self.lost or self.won:
            return
        self.guess.setPinColor(color, position1)
        print("Resetting pin " + str(position1) + " to be " + str(color))
        # find the original guess's corresponding clue to compare with
        if checkWhitePegs:
            newPegs = clue.getBlackPegs() - oldClue.getBlackPegs()
        else:
            newPegs = clue.getBlackPegs()
        print("Old pegs: " + str(oldPegs))
        print("New pegs: " + str(newPegs))
        # if the new clue has as many black pegs as the old clue...
        if newPegs >= oldPegs:
            # this means that the pin that had NOT been tested is in the correct position
            self.setPinAsConfirmed(position2)
        # if not, this means that the pin that HAD been tested had already been in the correct position
        else:
            self.setAsConfirmed(color, position1)

    """Tests the full code to find out which pins are in the correct locations. Used when the latest code received
    included three black pins."""

    def handleThreeBlack(self, checkWhitePins=False):
        print("Handling three black pins...")
        color1 = self.guess.getPin(0).color
        color2 = self.guess.getPin(1).color
        self.guess.setPinColor("", 0)
        clue = self.makeGuess(self.guess, True)
        if self.lost or self.won:
            return
        self.guess.setPinColor(color1, 0)
        if clue.getBlackPegs() == 3:
            for i in range(3):
                self.setPinAsConfirmed(i+1)
            self.handleOneUnknown()
            return
        else:
            self.guess.setPinColor("", 1)
            clue = self.makeGuess(self.guess, True)
            if self.lost or self.won:
                return
            self.guess.setPinColor(color2, 1)
            if clue.getBlackPegs() == 3:
                self.setPinAsConfirmed(0)
                self.setPinAsConfirmed(2)
                self.setPinAsConfirmed(3)
                self.handleOneUnknown()
                return
            else:
                self.setPinAsConfirmed(0)
                self.setPinAsConfirmed(1)
                self.test(2, 3, checkWhitePins, self.guessList[self.guessCount - 3])
                self.handleOneUnknown()
                return

    """Handles any situation where the most recent guess made had two pins set in the correct location."""

    def handleTwoUnknowns(self):
        print("Handling two unknowns...")
        if len(self.getUnconfirmedPositions()) < 2:
            self.handleOneUnknown()
            return
        position1 = self.getUnconfirmedPositions()[0]
        position2 = self.getUnconfirmedPositions()[1]
        receivedPins = False
        while not receivedPins:
            color1, color2 = randomTwoColors(self.viableColors)
            self.guess.setPinColor(color1, position1)
            self.guess.setPinColor(color2, position2)
            clue = self.makeGuess(self.guess)
            if self.lost or self.won:
                return
            wp = clue.getWhitePegs()
            bp = clue.getBlackPegs()
            if wp != 0 or bp > 2:
                receivedPins = True
            else:
                if color1 in self.viableColors:
                    self.viableColors.remove(color1)
                if color2 in self.viableColors:
                    self.viableColors.remove(color2)
        # once some pins have been received...
        if bp == 3:
            self.test(position1, position2)
            self.handleOneUnknown()
        else:
            if wp == 2:
                self.setAsConfirmed(color2, position1)
                self.setAsConfirmed(color1, position2)
                self.makeGuess(self.guess)
                return
            else:
                if wp == 1:
                    self.guess.swapPins(position1, position2)
                    self.test(position1, position2, True)
                    return

    """Handles any situation where there is only one incorrect pin, and its location is known."""

    def handleOneUnknown(self):
        if len(self.getUnconfirmedPositions()) < 1:
            return
        position = self.getUnconfirmedPositions()[0]
        clist = self.viableColors.copy()
        # remove as an option any colors that have been guessed and proven incorrect
        for guess in self.guessList:
            sameCode = True
            for i in range(4):
                if i != position:
                    if guess.getPin(i).color != self.guess.getPin(i).color:
                        sameCode = False
            if sameCode:
                if guess.getPin(position).color in clist:
                    clist.remove(guess.getPin(position).color)
        for color in clist:
            if not self.won and not self.lost:
                self.guess.setPinColor(color, position)
                self.makeGuess(self.guess)
        return True

    """Returns which positions (indices) in the code have not been confirmed yet."""

    def getUnconfirmedPositions(self):
        indexList = []
        count = 0
        for item in self.confirmedColors:
            if item == "":
                indexList.append(count)
            count += 1
        return indexList

    def getConfirmedPositions(self):
        available = self.getUnconfirmedPositions()
        unavailable = []
        for i in range(4):
            if i not in available:
                unavailable.append(i)
        return unavailable

    """"Calls the game manager to figure out the corresponding code for the given guess"""

    def makeGuess(self, guess=None, testing=False):
        if not testing:
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
        if self.guessCount > self.MAX_GUESSES:
            print("---Ran out of guesses!---")
            self.lost = True
            return clue
        if clue.getBlackPegs() == 4:
            print("Correct guess was made in " + str(self.guessCount) + " guesses!")
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
        while not self.won and not self.lost:
            self.createGuess()
            if not self.won and not self.lost:
                self.makeGuess()
        print("Done!")
        if self.won:
            return True
        else:
            return False
