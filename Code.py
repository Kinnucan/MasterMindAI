# a combination of four CodePins
import random
from CodePin import *
from Clue import *


def makeCode(numList):
    #given a list of integers from 1 to COLOR_NUMBER, creates a corresponding Code object
    #(for instance, [1,1,2,2] would return the code "red red orange orange", under the normal 4-peg, 6-color rules)
    if len(numList) != PIN_NUMBER:
        return None
    colorList = []
    for i in numList:
        if i-1 not in range(len(COLOR_NUMBER)):
            return None
        colorList.append(COLOR_LIST[i-1])
    return Code([CodePin(col) for col in colorList])


def generateNumberPermuations(K, P):
    allPermutations = []
    if P == 0:
        return allPermutations
    for i in range(1, K+1):
        allPermutations += [[i]+permuation for permuation in generateNumberPermuations(K, P-1)]
    return allPermutations

def generateAllCodes():
    return [makeCode(perm) for perm in generateNumberPermuations(COLOR_NUMBER, PIN_NUMBER)]





class Code:

    def __init__(self, pinList):
        self.isTest = False
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

    def getPin(self, position):
        return self.pinList[position]

    def setPin(self, pin, position):
        self.pinList[position] = pin

    def setPinColor(self, color, position):
        print("Setting pin " + str(position) + " to be " + str(color))
        newPin = CodePin(color)
        self.pinList[position] = newPin

    def swapPins(self, firstPosition, secondPosition):
        pin1 = self.getPin(firstPosition)
        pin2 = self.getPin(secondPosition)
        # if pin1.color == pin2.color:
        #     pin2.setColor("")  # the empty string will stand in for any color the program knows is not in the code
        self.setPin(pin1, secondPosition)
        self.setPin(pin2, firstPosition)

    def getColors(self):
        clist = []
        for pin in self.pinList:
            if pin.color not in clist:
                clist.append(pin.color)
        return clist

    # given a list of acceptable colors, return a list of yet unused, viable colors for guessing
    def getViableUnused(self, vlist):
        clist = vlist.copy()
        guessColors = self.getColors()
        for color in guessColors:
            if color in clist:
                clist.remove(color)
        return clist

    def setAsTest(self):
        self.isTest = True

    def removeAsTest(self):
        self.isTest = False

    def checkIfTest(self):
        return self.isTest

    def copy(self):
        newCode = Code([])
        for i in range(4):
            newCode.setPin(self.pinList[i], i)
        return newCode

    def cleanMatches(self):
        for pin in self.pinList:
            pin.unmatch()

    def getClue(self, guess):
        output = Clue()
        # check every pin to see if there are any exact (i.e., black) matches
        for i in range(PIN_NUMBER):
            codePin = self.getPinList()[i]
            guessPin = guess.getPinList()[i]
            if codePin.color == guessPin.color:
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
                    if codePin.color == guessPin.color:
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
            if pin.color == "":
                codeString = codeString + "null" + " "
            else:
                codeString = codeString + pin.color + " "
        return codeString

    def __eq__(self,other):
        return self.pinList == other.getPinList()
