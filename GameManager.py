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

    # process a guess (each guess will be compared with the manager's existing Code)
    def guessCode(self, guess):
        clues = []
        valid = True
        if not isinstance(guess, Code):
            print("The object provided is not a valid code.")
            valid = False
        if valid:
            # check every pin in the hidden code
            for pin in self.code:
                ind = self.code.index(pin)
                color = pin.color
                # run through all of the pins in the guess
                for otherPin in guess:
                    # if the pin has been previously matched, skip over it. Otherwise, check it
                    if not otherPin.matched:
                        otherInd = guess.index(otherPin)
                        otherColor = otherPin.color
                        if color.equals(otherColor):
                            if ind == otherInd:
                                # add a "red pin" to the clue list to indicate a perfect match exists
                                self.clues.append("red")
                            else:
                                # add a "white pin" to the clue list to indicate correct color, but wrong position
                                self.clues.append("white")
                            # denote the pin in the guess as having been matched
                            otherPin.matched = True
        # add the clues for this guess to the list of all clues returned over the course of the game
        self.clueList.append(clues)
        # add the guessed code to the list of all codes guessed
        self.guessList.append(guess)
        return clues
