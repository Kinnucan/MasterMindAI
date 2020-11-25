# a combination of four CodePins
import random
from CodePin import *
from Clue import *




class Code:

    def __init__(self, pinList):
        self.pinList = pinList # what will hold the code (order matters)
        # if given an empty list, create a random code
        if len(pinList) == 0:
            self.randomize()
        else:
            valid = True
            for pin in pinList:
                if type(pin) != CodePin:
                    print("Given list contains at least one item that is not a CodePin.")
                    valid = False
                elif len(pinList) != PIN_NUMBER:
                    print("Given list has wrong number of pins.")
                    valid = False
            if valid:
                self.pinList = pinList

    # create a random code
    def randomize(self):
        # each loop adds a pin of a random color to pinList
        self.pinList = []
        for x in range(PIN_NUMBER):
            num = random.randrange(0, COLOR_NUMBER)
            self.pinList.append(CodePin(COLOR_LIST[num]))

    def getPinList(self):
        return self.pinList

    def cleanMatches(self):
        for pin in self.pinList:
            pin.unmatch()

    def getClue(self, guess):
        output = Clue()
        # check every pin to see if there are any exact (i.e., black) matches
        for i in range(PIN_NUMBER):
            codePin = self.getPinList()[i]
            guessPin = guess.getPinList()[i]
            if codePin == guessPin:
                # add a "black pin" to the clue to indicate a perfect match exists
                output.augmentBlackPegs()
                # denote the pins as having been matched
                guessPin.match()
                codePin.match()
        # check every pin in the hidden code to see if there are any inexact (i.e., white) matches
        for codeInd in range(PIN_NUMBER):
            codePin = self.getPinList()[codeInd]
            # run through all of the pins in the guess
            for guessInd in range(PIN_NUMBER):
                guessPin = guess.getPinList()[guessInd]
                # if the pin has been previously matched, skip over it. Otherwise, check it
                if not (guessPin.matched or codePin.matched):
                    if codePin == guessPin:
                        if codeInd != guessInd:
                            # add a "white pin" to the clue list to indicate correct color, but wrong position
                            output.augmentWhitePegs()
                            # denote the pins as having been matched
                            guessPin.match()
                            codePin.match()
        # we don't need the matchings anymore
        guess.cleanMatches()
        self.cleanMatches()
        return output

    # print out the colors of each of the pins in the code
    def __str__(self):
        codeString = ""
        for pin in self.pinList:
            codeString = codeString + pin.color + " "
        return codeString

    def __eq__(self,other):
        return self.pinList == other.getPinList()
