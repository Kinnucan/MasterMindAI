# a combination of four CodePins
import random
from CodePin import CodePin


class Code:
    colorList = ["red", "orange", "yellow", "green", "blue", "purple"]  # a list of the six acceptable colors
    pinList = [] # what will hold the code (order matters)

    def __init__(self, pinList):
        # if given an empty list, create a random code
        if len(pinList) == 0:
            self.randomize()
        else:
            valid = True
            for pin in pinList:
                if type(pin) != CodePin:
                    print("Given list contains at least one item that is not a CodePin.")
                    valid = False
            if valid:
                self.pinList = pinList

    # create a random code
    def randomize(self):
        # each loop adds a pin of a random color to pinList
        for x in range(4):
            num = random.randrange(0, 6)
            if num == 0:
                self.pinList.append(CodePin("red"))
            else:
                if num == 1:
                    self.pinList.append(CodePin("orange"))
                else:
                    if num == 2:
                        self.pinList.append(CodePin("yellow"))
                    else:
                        if num == 3:
                            self.pinList.append(CodePin("green"))
                        else:
                            if num == 4:
                                self.pinList.append(CodePin("blue"))
                            else:
                                self.pinList.append(CodePin("purple"))

    # set the code
    def setCode(self, code):
        pinList = []
        for pin in code:
            if not isinstance(pin, CodePin):
                print("Please enter a list of pins.")
                # TODO: Add an error call here
            else:
                pinList.append(pin)
        self.pinList = pinList

    # print out the colors of each of the pins in the code
    def printCode(self):
        codeString = ""
        for pin in self.pinList:
            codeString = codeString + pin.color + " "
        print(codeString)
