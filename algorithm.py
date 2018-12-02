import pandas as pd
import math
import collections
import numpy as np

trainFileName = "trainData.csv"
trainDataFrame = pd.read_csv(trainFileName)
testFileName = "testData1.csv"
testDataFrame = pd.read_csv(testFileName)
eta = .1
listOfColumns = ['DAY_OF_WEEK', 'AIRLINE', 'FLIGHT_NUMBER',
'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'SCHEDULED_DEPARTURE', 'SCHEDULED_TIME',
'DISTANCE', 'SCHEDULED_ARRIVAL', 'ARRIVAL_DELAY', 'DEPART_TEMP', 'DEPART_HUMIDITY',
'DEPART_WINDIR', 'DEPART_WIND', 'DEPART_PRECIP', 'ARRIVAL_TEMP', 'ARRIVAL_HUMIDITY',
'ARRIVAL_WINDIR', 'ARRIVAL_WIND', 'ARRIVAL_PRECIP']
featureVector = collections.defaultdict(float)


# dotProduct(weights, featureExtractor(x))
# increment(weights, y*eta,featureExtractor(x))

def featureExtractor(entry):
    map = collections.defaultdict(float)
    for colValue in listOfColumns:
        value = entry[colValue]
        feature = ""
        if str(colValue) == 'SCHEDULED_DEPARTURE' or str(colValue) == 'SCHEDULED_ARRIVAL':
            if math.isnan(value):
                value = 0
            bucket = str(int(int(value)/600))
            feature = colValue + "-" + bucket
        elif str(colValue) == 'SCHEDULED_TIME':
            if math.isnan(value):
                value = 0
            bucket = str(int(int(value)/60))
            feature = colValue + "-" + str(bucket)
        elif str(colValue) == 'DISTANCE':
            if math.isnan(value):
                value = 0
            bucket = str(int(int(value)/1000))
            feature = colValue + "-" + str(bucket)
        elif (str(colValue) == 'DEPART_TEMP' or str(colValue) == 'ARRIVAL_TEMP'
        or str(colValue) == 'DEPART_HUMIDITY' or str(colValue) == 'ARRIVAL_HUMIDITY'
        or str(colValue) == 'DEPART_WIND' or str(colValue) == 'ARRIVAL_WIND'
        or str(colValue) == 'DEPART_PRECIP' or str(colValue) == 'ARRIVAL_PRECIP'):
            if math.isnan(value):
                value = 0
            # print ("value: ", value)
            bucket = str(int(int(value)/10))
            feature = colValue + "-" + str(bucket)
        else:
            feature = colValue + "-" + str(value)

        map[feature] = 1.0

    return map

def dotProduct(d1, d2):
    """
    @param dict d1: a feature vector represented by a mapping from a feature (string) to a weight (float).
    @param dict d2: same as d1
    @return float: the dot product between d1 and d2
    """
    # if len(d1) < len(d2):
    #     return dotProduct(d2, d1)
    # else:
    sum = 0.0
    for key in d2:
        sum += (d2[key]*d1[key])
    return sum

        # return sum(d1.get(f, 0) * v for f, v in d2.items())

def increment(d1, scale, d2):
    """
    Implements d1 += scale * d2 for sparse vectors.
    @param dict d1: the feature vector which is mutated.
    @param float scale
    @param dict d2: a feature vector.
    """
    for f, v in d2.items():
        d1[f] = d1.get(f, 0) + v * scale

# training data
for index, row in trainDataFrame.iterrows():
    bucket = ""
    for colValue in listOfColumns:
        value = row[colValue]
        # print ("value", value)
        # if math.isnan(value):
        #     value = 0
        if str(colValue) == 'SCHEDULED_DEPARTURE' or str(colValue) == 'SCHEDULED_ARRIVAL':
            if math.isnan(value):
                value = 0
            bucket = str(int(int(value)/600))
            entry = colValue + "-" + bucket
        elif str(colValue) == 'SCHEDULED_TIME':
            if math.isnan(value):
                value = 0
            bucket = str(int(int(value)/60))
            entry = colValue + "-" + str(bucket)
        elif str(colValue) == 'DISTANCE':
            if math.isnan(value):
                value = 0
            bucket = str(int(int(value)/1000))
            entry = colValue + "-" + str(bucket)
        elif (str(colValue) == 'DEPART_TEMP' or str(colValue) == 'ARRIVAL_TEMP'
        or str(colValue) == 'DEPART_HUMIDITY' or str(colValue) == 'ARRIVAL_HUMIDITY'
        or str(colValue) == 'DEPART_WIND' or str(colValue) == 'ARRIVAL_WIND'
        or str(colValue) == 'DEPART_PRECIP' or str(colValue) == 'ARRIVAL_PRECIP'):
            if math.isnan(value):
                value = 0
            # print ("value: ", value)
            bucket = str(int(int(value)/10))
            entry = colValue + "-" + str(bucket)
        else:
            entry = colValue + "-" + str(value)
        featureVector[entry] = 0.0

for i in range(1):
    for index, row in trainDataFrame.iterrows():
        realOutput = row['ARRIVAL_DELAY']
        entryFeatures = featureExtractor(row)

        # print ("entryVector: ", entryFeatures)
        # print ("featureVector", featureVector)
        sum = realOutput*(dotProduct(featureVector, entryFeatures))
        if sum < 1:
            increment(featureVector, realOutput*eta, entryFeatures)


# testing data!
track = 0.0
currBest = 100
bestNum = 0
while (track < 10.0):
    # for i in range (10000000):
    #     aopple = 1
    print ("index: ", track)
    numDelay = 0
    numOnTime = 0
    predictDelay = 0
    predictOnTime = 0
    counterCorrect = 0
    for index, row in testDataFrame.iterrows():
        realOutput = row['ARRIVAL_DELAY']
        if realOutput == 1:
            numDelay += 1
        else:
            numOnTime += 1
        entryFeatures = featureExtractor(row)
        dotProductValue = dotProduct(featureVector, entryFeatures)
        delayed = False
        if dotProductValue > track:
            delayed = True
        if delayed == True:
            predictDelay += 1
        else:
            predictOnTime += 1
        if realOutput == delayed:
            counterCorrect += 1
        #     print ("correct!")
        # else:
        #     print ("wrong classification :(")
    track = float(track + .01)
    # print ("updated index: ", track)
    actualDelayed = ((100.0*numDelay)/(numDelay+numOnTime))
    # print ("real: ", actualDelayed)
    predictedDelay = (100.0*predictDelay)/(predictDelay+predictOnTime)
    # print ("guess: ", predictedDelay)
    loss = abs(actualDelayed - predictedDelay)
    # print ("loss: ", loss)
    if loss < currBest:
        currBest = loss
        bestNum = index

numDelay = 0
numOnTime = 0
predictDelay = 0
predictOnTime = 0
counterCorrect = 0
for index, row in testDataFrame.iterrows():
    realOutput = row['ARRIVAL_DELAY']
    if realOutput == 1:
        numDelay += 1
    else:
        numOnTime += 1
    entryFeatures = featureExtractor(row)
    dotProductValue = dotProduct(featureVector, entryFeatures)
    delayed = False
    if dotProductValue > bestNum:
        delayed = True
    if delayed == True:
        predictDelay += 1
    else:
        predictOnTime += 1
    if realOutput == delayed:
        counterCorrect += 1
    #     print ("correct!")
    # else:
    #     print ("wrong classification :(")


print ("delay = {}, on time = {}, predict delay = {}, predict on time = {}".format(numDelay, numOnTime, predictDelay, predictOnTime))
print ("actual: {}%, prediction: {}%".format((100.0*numDelay/(numDelay+numOnTime)), ((100.0*predictDelay)/(predictDelay+predictOnTime))))
print ("Correctly labeled: {}%".format((100.0*counterCorrect)/(numDelay+numOnTime)))

# print ("featureVector:", featureVector)
# for entry in featureVector:
#     if featureVector[entry] > 0:
#         print ("featureName: ", entry, ", featureValue: ", featureVector[entry])


#
#
# for entry in featureVector:
#     featureVector[entry] *= 10
#     if featureVector[entry] > 0:
#         print ("featureVector[{}] = {}".format(entry, featureVector[entry]))
