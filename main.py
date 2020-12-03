# import necessary classes
from GameManager import *
from CodePin import *
from Code import *

from Agents.RandomAgent import *
from Agents.RandomEligibleAgent import *
from Agents.Player import *


def environmentTests():
    testCode = Code([])
    # print(testCode)
    manager = GameManager(testCode)
    # print(manager.guessCode(testCode))

    testCode2 = Code([CodePin("purple"), CodePin("orange"), CodePin("yellow"), CodePin("blue")])
    manager2 = GameManager(testCode2)
    guess2 = Code([CodePin("yellow"), CodePin("orange"), CodePin("yellow"), CodePin("blue")])
    print(manager2.guessCode(guess2))
    print(manager2.guessCode(guess2))

    for i in range(10):
        x, y = Code([]), Code([])
        print(x.getClue(y) == y.getClue(x))


def simpleAgentTests():
    newGame = GameManager()
    randy = RandomAgent(newGame, verbose=True)
    randy.play()
    print("---------------------")
    newGame = GameManager()
    you = HumanAgent(newGame)
    you.play()

def betterAgentTests():
    newGame = GameManager()
    randy2 = RandomEligibleAgent(newGame, verbose=True)
    randy2.play()


if __name__ == '__main__':
    #environmentTests()
    #simpleAgentTests()
    betterAgentTests()



