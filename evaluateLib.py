import re

REGEX_PATTERN_TIMESTAMP = '^\/\/#! Time: ([\d|.| |:]*)'
REGEX_PATTERN_TEST = '\/\/## ([A-z]*):[ ]*[.|/]*([A-z]*)'


class Datapoint(object):
    def __init__(self, timestamp, tests):
        self.Timestamp = timestamp
        self.Tests = tests


class Test(object):
    def __init__(self, name):
        self.Name = name


class SpeedTest(Test):
    CoreCommand = "speedtest"

    def __init__(self, name, tstString):
        super().__init__(name)

        self.DownloadMbits = float(
            re.search('Download: (\d*\.?\d*) Mbit/s', tstString).group(1))
        self.UploadMbits = float(
            re.search('Upload: (\d*\.?\d*) Mbit/s', tstString).group(1))

class PingTest(Test):
    CoreCommand = "ping"

    def __init__(self, name, tstString):
        super().__init__(name)


        self.PercentPacketLoss = int(
            re.search('received, (\d*)% packet loss', tstString).group(1))
        if(self.PercentPacketLoss != 100):
            self.PingAvgMs = float(
                re.search('rtt min\/avg\/max\/mdev = \d*\.?\d*\/(\d*\.?\d*)\/\d*', tstString).group(1))
        else:
            self.PingAvgMs = 10000.0 #Dummy Value for ping unsucessfull

availableTestTypes = {}
availableTestTypes[SpeedTest.CoreCommand] = lambda n, s: SpeedTest(n, s)
availableTestTypes[PingTest.CoreCommand] = lambda n, s: PingTest(n, s)


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

    if(coreCommand not in availableTestTypes):
        print("No test type available for coreCommand " + coreCommand)
        return None

    testType = availableTestTypes[coreCommand]
    return testType(name, tstString)


def parseDatapoint(dpString):
    timestamp = re.search(REGEX_PATTERN_TIMESTAMP, dpString).group(1)

    testStrings = findSubstringsStartingWith(dpString, '//##')
    tests = list(map(parseTest, testStrings))
    return Datapoint(timestamp, tests)


def parseResultString(resultString):
    dataPointStrings = findSubstringsStartingWith(resultString, '//#!')

    datapoints = list(map(parseDatapoint, dataPointStrings))
    return datapoints
