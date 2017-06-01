from NeuralNetUtil import buildExamplesFromCarData,buildExamplesFromPenData, getXORData, getBalanceData
from NeuralNet import buildNeuralNet
import cPickle 
from math import pow, sqrt

def average(argList):
    return sum(argList)/float(len(argList))

def stDeviation(argList):
    mean = average(argList)
    diffSq = [pow((val-mean),2) for val in argList]
    return sqrt(sum(diffSq)/len(argList))

penData = buildExamplesFromPenData() 
def testPenData(hiddenLayers = [24]):
    return buildNeuralNet(penData,maxItr = 200, hiddenLayerList =  hiddenLayers)

carData = buildExamplesFromCarData()
def testCarData(hiddenLayers = [16]):
    return buildNeuralNet(carData,maxItr = 200,hiddenLayerList =  hiddenLayers)

XORData = getXORData()
def testXORData(hiddenLayers = [3]):
    return buildNeuralNet(XORData, maxItr=5000, hiddenLayerList=hiddenLayers)

balanceData = getBalanceData()

def testBalanceData(hiddenLayers = [16]):
    return buildNeuralNet(balanceData,maxItr = 200,hiddenLayerList =  hiddenLayers)


if __name__ == "__main__":
#     testCarData()
#     print "tested XOR"
#     testXORData()
#     print "testing XOR"

    balanceAccuracy = []

    # question 5 analysis
    for i in range(0, 5):
        nnetBalance, testAccuracyBalance = testBalanceData()
        balanceAccuracy.append(testAccuracyBalance)


    balanceSD = stDeviation(balanceAccuracy)
    balanceAvg = average(balanceAccuracy)

    print "balanceSD: " + str(balanceSD)
    print "balanceAvg: " + str(balanceAvg)
    print "balanceAccuracy: " + str(balanceAccuracy)


#     getBalanceData()
#     # carData = buildExamplesFromCarData()
#     testBalanceData()
#
#     carAccuracy = []
#     penAccuracy = []
#
#     # question 5 analysis
#     for i in range(0, 5):
#         nnetCar, testAccuracyCar = testCarData()
#         carAccuracy.append(testAccuracyCar)
#         nnetPen, testAccuracyPen = testPenData()
#         penAccuracy.append(testAccuracyPen)
#
#     carSD = stDeviation(carAccuracy)
#     penSD = stDeviation(penAccuracy)
#     carAvg = average(carAccuracy)
#     penAvg = average(penAccuracy)
#
#     print "carSD: " + str(carSD)
#     print "carAvg: " + str(carAvg)
#     print "carAccuracy: " + str(carAccuracy)
#     print "penSD: " + str(penSD)
#     print "penAvg: " + str(penAvg)
#     print "penAccuracy: " + str(penAccuracy) + "\n"

    #question 6 analysis:
    penAccuracy = []
    numNeurons = 0
    while numNeurons <= 40:
        for i in range(0, 5):
            nnetPen, testAccuracyPen = testPenData(hiddenLayers = [numNeurons])
            penAccuracy.append(testAccuracyPen)

        penSD = stDeviation(penAccuracy)
        penAvg = average(penAccuracy)
        print "penIteration: " + str(numNeurons/5)
        print "penSD: " + str(penSD)
        print "penAvg: " + str(penAvg)
        print "penAccuracy: " + str(penAccuracy) + "\n"
        penAccuracy = []
        numNeurons += 5

    q6(testPenData)












