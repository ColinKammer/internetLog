import sys

import evaluateLib


def main():
    if(len(sys.argv) != 2):
        print('Invalid call - Syntax: python evaluate.py <resultFile>\n')
        return
    resultFile = sys.argv[1]

    print('Opening File\n')
    with open(resultFile, 'r') as file:
        resultString = file.read()

    print('Parsing Results\n')
    parsedResult = evaluateLib.parseResultString(resultString)

    print('Found {} Datapoints (Time based Records)\n'.format(len(parsedResult)))


if __name__ == '__main__':
    main()
