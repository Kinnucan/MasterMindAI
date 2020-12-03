# colored pins which constitute a code

COLOR_LIST = ["red", "orange", "yellow", "green", "blue", "purple"] # a list of the six acceptable colors
COLOR_NUMBER = len(COLOR_LIST)
PIN_NUMBER = 4


class CodePin:

    def __init__(self, color):
        self.color = ""
        self.matched = False  # whether or not the pin has been matched when checking codes against one another

        # if the color provided is invalid, return message
        if color in COLOR_LIST:
            self.color = color
        else:
            print(color + " is not a valid color.")

    def match(self):
        self.matched = True

    def unmatch(self):
        self.matched = False

    def getColor(self):
        return self.color

    def __str__(self):
        return self.color + " peg"

    def __eq__(self, other):
        return self.color == other.getColor()
