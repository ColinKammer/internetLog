import re

REGEX_PATTERN_TIMESTAMP = '^\/\/#! Time: ([\d|.| |:]*)'
REGEX_PATTERN_TEST = '\/\/## ([A-z]*):[ ]*[.|/]*([A-z]*)'


class Datapoint:
    def __init__(self, timestamp, tests):
        self.Timestamp = timestamp
        self.Tests = tests


class Test:
    def __init__(self, name, coreCommand, measuredValues):
        self.Name = name
        self.CoreCommand = coreCommand
        self.MeasuredValues = measuredValues


def findSubstringsStartingWith(string, partStartSequence):
    """ This find substrings starting with the given sequence
        (Non Overlapping)"""

    parts = []

    currentIndex = string.find(partStartSequence, 0)
    nextIndex = string.find(partStartSequence, currentIndex+1)

    while (nextIndex != -1):
        parts.append(string[currentIndex:nextIndex])
        currentIndex = nextIndex
        nextIndex = string.find(partStartSequence, currentIndex+1)

    # Last part is limited by EOF
    parts.append(string[currentIndex:])
    return parts


def parseTest(tstString):
    name = re.search(REGEX_PATTERN_TEST, tstString).group(1)
    coreCommand = re.search(REGEX_PATTERN_TEST, tstString).group(2)

    return Test(name, coreCommand, [])


def parseDatapoint(dpString):
    timestamp = re.search(REGEX_PATTERN_TIMESTAMP, dpString).group(1)

    testStrings = findSubstringsStartingWith(dpString, '//##')
    tests = list(map(parseTest, testStrings))
    return Datapoint(timestamp, tests)


def parseResultString(resultString):
    dataPointStrings = findSubstringsStartingWith(resultString, '//#!')

    datapoints = list(map(parseDatapoint, dataPointStrings))
    return datapoints
