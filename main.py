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
from Agents.LexicographicAgent import *

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
    randy2 = RandomEligibleAgent(newGame, verbose=True)
    randy2.play()
    newGame = GameManager()
    wordgirl = LexicographicAgent(newGame, verbose=True)
    wordgirl.play()

def geneticAlgortihmTest():
    newGame = GameManager()
    genny = GeneticAlgorithmAgent(newGame, verbose=True, firstGuess=makeCode([1,1,2,2]))
    genny.play()


def knuthAgentTest():
    newGame = GameManager()
    knuth = Knuth(newGame, verbose=True)
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
    """
    A series of tests written to see how our code works.
    environmentTests just makes sure that our GameManager object runs as expected -- that it can create a code and respond to guesses as expected.
    simpleAgentTests tests the very primitive Mastermind AIs we wrote. Those AIs were mainly intended to make sure we had coded the Agent object correctly; they do not play Mastermind well.
    betterAgentTests tests some simple, but effective Mastermind AIs. They are good AIs, but they were not the focus of our project.
    geneticAlgorithmTest, humanAgentTest, and knuthAgentTest all test the AIs we wrote for this project.
    Note that because "Felix" interacts with GameManager slightly differently than the other AIs, its testing function is different too.
    """
    environmentTests()
    simpleAgentTests()
    betterAgentTests()
    geneticAlgortihmTest()
    humanAgentTests()
    knuthAgentTest()

