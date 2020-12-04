import re
import datetime

TIMESTAMP_FORMAT = '%d.%m.%Y %H:%M:%S'

REGEX_PATTERN_TIMESTAMP = '^\/\/#! Time: ([\d|.| |:]*)'
REGEX_PATTERN_TEST = '\/\/## ([A-z]*):[ ]*[.|/]*([A-z]*)'


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
        matchDownload = re.search('Download: (\d*\.?\d*) Mbit/s', tstString)
        matchUpload = re.search('Upload: (\d*\.?\d*) Mbit/s', tstString)
        
        if((matchDownload is None) or (matchUpload is None)):
            self.DownloadMbits = 0
            self.UploadMbits = 0
            self.Failure = True
        else:
            self.DownloadMbits = float(matchDownload.group(1))
            self.UploadMbits = float(matchUpload.group(1))


class PingTest(Test):
    CoreCommand = "ping"

    def __init__(self, name, tstString):
        super().__init__(name)

        matchPacketloss = re.search('received, (\d*)% packet loss', tstString)
        matchAvgPing = re.search('rtt min\/avg\/max\/mdev = \d*\.?\d*\/(\d*\.?\d*)\/\d*', tstString)

        if(matchPacketloss is None):
            #raise Exception("unable to find packet loss")
            self.PercentPacketLoss = 100
        else:
            self.PercentPacketLoss = int(matchPacketloss.group(1))

        if(matchAvgPing is None):
            self.PingAvgMs = 10000.0  # Dummy Value for ping unsucessfull
        else:
            self.PingAvgMs = float(matchAvgPing.group(1))
            

availableTestTypes = {}
availableTestTypes[SpeedTest.CoreCommand] = lambda n, s: SpeedTest(n, s)
availableTestTypes[PingTest.CoreCommand] = lambda n, s: PingTest(n, s)


def parseTest(tstString):
    name = re.search(REGEX_PATTERN_TEST, tstString).group(1)
    coreCommand = re.search(REGEX_PATTERN_TEST, tstString).group(2)

    if(coreCommand not in availableTestTypes):
        print("No test type available for coreCommand " + coreCommand)
        return None

    testType = availableTestTypes[coreCommand]
    return testType(name, tstString)


def parseDatapoint(dpString):
    timestampStr = re.search(REGEX_PATTERN_TIMESTAMP, dpString).group(1)
    timestamp = datetime.datetime.strptime(timestampStr, TIMESTAMP_FORMAT)

    testStrings = findSubstringsStartingWith(dpString, '//##')
    tests = list(map(parseTest, testStrings))
    return Datapoint(timestamp, tests)


def parseResultString(resultString):
    dataPointStrings = findSubstringsStartingWith(resultString, '//#!')

    datapoints = list(map(parseDatapoint, dataPointStrings))
    return datapoints
