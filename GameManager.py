# The manager of the Mastermind environment
from Code import Code


class GameManager:

    code = []
    guessList = []
    clueList = []

    # generate a randomized code
    def generateCode(self):
        self.code = Code([])

    # process a guess (each guess will be compared with the manager's existing Code)
    def guessCode(self, guess):
        valid = True
        if not isinstance(guess, Code):
            print("The object provided is not a valid code.")
            valid = False

