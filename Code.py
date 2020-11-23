# a combination of four CodePins
import random
from MasterMind.CodePin import *


PIN_NUMBER = 4

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

    # print out the colors of each of the pins in the code
    def __str__(self):
        codeString = ""
        for pin in self.pinList:
            codeString = codeString + pin.color + " "
        return codeString

    def __eq__(self,other):
        return self.pinList == other.getPinList()
