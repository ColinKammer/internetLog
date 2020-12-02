import evaluateParseLib as evalParse


def calcAverageDownloadSpeed(parsedResult):
    speeds = list(map(lambda x: x.Tests[0].DownloadMbits, parsedResult))
    return sum(speeds)/len(speeds)


def calcAverageUploadSpeed(parsedResult):
    speeds = list(map(lambda x: x.Tests[0].UploadMbits, parsedResult))
    return sum(speeds)/len(speeds)


def calcAveragePacketlossPerDatapoint(datapoint):
    sum = 0.0
    count = 0
    for test in datapoint.Tests:
        if(isinstance(test, evalParse.PingTest)):
            sum += test.PercentPacketLoss
            count += 1
    return sum/count


def getTimeStampOfDatapoint(datapoint):
    return datapoint.Timestamp
