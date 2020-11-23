# import necessary classes
from MasterMind.GameManager import *
from MasterMind.CodePin import *
from MasterMind.Code import *

from MasterMind.Agents.RandomAgent import *
from MasterMind.Agents.HumanAgent import *


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


def simpleAgentTests():
    newGame = GameManager()
    randy = RandomAgent(newGame, verbose=True)
    randy.play()
    print("---------------------")
    newGame = GameManager()
    you = HumanAgent(newGame)
    you.play()



if __name__ == '__main__':
    simpleAgentTests()



