# import necessary classes
from GameManager import *
from CodePin import *
from Code import *

from Agents.RandomAgent import *
from Agents.HumanAgent import *
from Agents.Knuth import *
from Agents.RandomEligibleAgent import *
from Agents.Player import *
from Agents.GeneticAlgorithmAgent import *

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
    you = Player(newGame)
    you.play()

def betterAgentTests():
    newGame = GameManager()
    # randy2 = RandomEligibleAgent(newGame, verbose=True)
    # randy2.play()
    genny = GeneticAlgorithmAgent(newGame, verbose=True, firstGuess=makeCode([1,1,2,3]), EHatChoiceMethod="random",maxGen=50)
    genny.play()


def knuthAgentTest():
    newGame = GameManager()
    knuth = Knuth(newGame)
    knuth.play()

def humanAgentTests():
    winCounter = 0
    for i in range(100):
        newGame = GameManager()
        agent = HumanAgent(newGame)
        if agent.go():
            winCounter += 1
    print("Agent won " + str(winCounter) + " out of 100 times!")


if __name__ == '__main__':
    # environmentTests()
    # simpleAgentTests()
    # humanAgentTests()
    knuthAgentTest()
    # betterAgentTests()
