# colored pins which constitute a code

class CodePin:
    colorList = ["red", "orange", "yellow", "green", "blue", "purple"] # a list of the six acceptable colors
    color = ""
    matched = False  # whether or not the pin has been matched when checking codes against one another

    def __init__(self, color):
        # if the color provided is invalid, return message
        if color in self.colorList:
            self.color = color
        else:
            print(color + " is not a valid color.")

    def match(self):
        self.matched = True
