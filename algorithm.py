import pandas as pd
import math
import collections
import numpy as np

fileName = "datapoints.csv"
dataFrame = pd.read_csv(fileName)
eta = .1
listOfColumns = ['YEAR', 'MONTH', 'DAY', 'DAY_OF_WEEK', 'AIRLINE', 'FLIGHT_NUMBER',
'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'SCHEDULED_DEPARTURE', 'SCHEDULED_TIME',
'DISTANCE', 'SCHEDULED_ARRIVAL', 'ARRIVAL_DELAY', 'DEPART_TEMP', 'DEPART_HUMIDITY',
'DEPART_WINDDIR', 'DEPART_WIND', 'DEPART_PRECIP', 'ARRIVAL_TEMP', 'ARRIVAL_HUMIDITY',
'ARRIVAL_WINDDIR', 'ARRIVAL_WIND', 'ARRIVAL_PRECIP']
featureVector = collections.defaultdict(float)


# dotProduct(weights, featureExtractor(x))
# increment(weights, y*eta,featureExtractor(x))

def featureExtractor(entry):
    map = collections.defaultdict(float)
    for colValue in listOfColumns:
        value = entry[colValue]
        map[colValue + "-" + str(value)] = 1.0

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



for index, row in dataFrame.iterrows():
    for colValue in listOfColumns:
        value = row[colValue]
        entry = colValue + "-" + str(value)
        featureVector[entry] = 0.0

for i in range(1000):
    for index, row in dataFrame.iterrows():
        realOutput = row['ARRIVAL_DELAY']
        entryFeatures = featureExtractor(row)

        # print ("entryVector: ", entryFeatures)
        # print ("featureVector", featureVector)
        sum = realOutput*(dotProduct(featureVector, entryFeatures))
        if sum < 1:
            increment(featureVector, realOutput*eta, entryFeatures)

# testing data!
numDelay = 0
numOnTime = 0
predictDelay = 0
predictOnTime = 0
counterCorrect = 0
for index, row in dataFrame.iterrows():
    realOutput = row['ARRIVAL_DELAY']
    if realOutput == 1:
        numDelay += 1
    else:
        numOnTime += 1
    entryFeatures = featureExtractor(row)
    dotProductValue = dotProduct(featureVector, entryFeatures)
    delayed = False
    if dotProductValue > 1.5:
        delayed = True
    if delayed == True:
        predictDelay += 1
    else:
        predictOnTime += 1
    if realOutput == delayed:
        counterCorrect += 1
        print ("correct!")
    else:
        print ("wrong classification :(")

print ("delay = {}, on time = {}, predict delay = {}, predict on time = {}".format(numDelay, numOnTime, predictDelay, predictOnTime))
print ("actual: {}%, prediction: {}%".format((100.0*numDelay/(numDelay+numOnTime)), ((100.0*predictDelay)/(predictDelay+predictOnTime))))
print ("Correctly labeled: {}%".format((100.0*counterCorrect)/(numDelay+numOnTime)))


#
#
# for entry in featureVector:
#     featureVector[entry] *= 10
#     if featureVector[entry] > 0:
#         print ("featureVector[{}] = {}".format(entry, featureVector[entry]))
