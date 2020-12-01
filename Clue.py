from CodePin import *



class Clue:
    def __init__(self, blackPegs = 0, whitePegs = 0):
        self.blackPegs = blackPegs
        self.whitePegs = whitePegs

    def getBlackPegs(self):
        return self.blackPegs

    def getWhitePegs(self):
        return self.whitePegs

    def augmentBlackPegs(self):
        self.blackPegs+=1

    def augmentWhitePegs(self):
        self.whitePegs+=1

    def isWinning(self):
        return self.blackPegs >= PIN_NUMBER

    def __str__(self):
        return str(self.blackPegs) + " black, " + str(self.whitePegs) + " white"

    def __eq__(self, other):
        return (self.getBlackPegs() == other.getBlackPegs() and self.getWhitePegs() == other.getWhitePegs())