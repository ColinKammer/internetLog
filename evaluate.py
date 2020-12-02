import sys

import matplotlib.pyplot as plt

import evaluateParseLib as evalParse
import evaluateUtilLib as evalUtil


def main():
    if(len(sys.argv) != 2):
        print('Invalid call - Syntax: python evaluate.py <resultFile>\n')
        return
    resultFile = sys.argv[1]

    print('Opening File\n')
    with open(resultFile, 'r') as file:
        resultString = file.read()

    print('Parsing Results\n')
    parsedResult = evalParse.parseResultString(resultString)

    print('Found {} Datapoints (Time based Records)\n'.format(len(parsedResult)))
    print('Avgerage Download-Speed (Mbit/s): {}\n'.format(
        evalUtil.calcAverageDownloadSpeed(parsedResult)))
    print('Avgerage Upload-Speed (Mbit/s): {}\n'.format(evalUtil.calcAverageUploadSpeed(parsedResult)))

    # Print Average Packet loss over Time
    x = list(map(evalUtil.getTimeStampOfDatapoint, parsedResult))
    y = list(map(evalUtil.calcAveragePacketlossPerDatapoint, parsedResult))

    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    main()
