# The manager of the Mastermind environment
from Code import Code


class GameManager:
    # the hidden code
    code = []
    # the list of all codes guessed over the course of the game
    guessList = []
    # the list of all clues returned over the course of the game
    clueList = []

    # generate a randomized code
    def generateCode(self):
        self.code = Code([])

    # manually set the manager's code
    def setCode(self, code):
        self.code = code

    # process a guess (each guess will be compared with the manager's existing Code)
    def guessCode(self, guess):
        clues = []
        valid = True
        if not isinstance(guess, Code):
            print("The object provided is not a valid code.")
            valid = False
        if valid:
            guessList = guess.pinList
            # make sure all pins are not set as matched
            for pin in self.code.pinList:
                pin.matched = False
            # check every pin in the hidden code once for perfect matches
            for pin in self.code.pinList:
                ind = self.code.pinList.index(pin)
                color = pin.color
                # run through all of the pins in the guess
                for otherPin in guessList:
                    # if the pin has been previously matched, skip over it. Otherwise, check it
                    if not otherPin.matched:
                        otherInd = guessList.index(otherPin)
                        otherColor = otherPin.color
                        if color == otherColor:
                            if ind == otherInd:
                                # add a "red pin" to the clue list to indicate a perfect match exists
                                clues.append("red")
                            # denote both pins as having been matched
                            pin.matched = True
                            otherPin.matched = True
            # check every pin a second time for imperfect matches
            for pin in self.code.pinList:
                if not pin.matched:
                    color = pin.color
                    # run through the pins in the guess again
                    for otherPin in guessList:
                        # skip if checked. Otherwise...
                        if not otherPin.matched:
                            otherColor = otherPin.color
                            if color == otherColor:
                                # add a "white pin" to the clue list to indicate matching colors at different indices
                                clues.append("white")
                                # denote the pins as having been matched
                                pin.matched = True
                                otherPin.matched = True
        # add the clues for this guess to the list of all clues returned over the course of the game
        self.clueList.append(clues)
        # add the guessed code to the list of all codes guessed
        self.guessList.append(guess)
        return clues
