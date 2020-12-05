import datetime

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

import csvTable

TIMESTAMP_FORMAT = '%d.%m.%Y %H:%M:%S'


def main():
    filterGraphs = True

    csv = csvTable.readFile('out.csv')

    timeStamps = list(map(
        lambda x: datetime.datetime.strptime(x, TIMESTAMP_FORMAT),
        csv.RowNames)
    )

    downloadSpeeds = csv.GetColumnByName('Speedtest_download[Mbit/s]')
    uploadSpeeds = csv.GetColumnByName('Speedtest_upload[Mbit/s]')

    pingTimes = np.average(
        csv.GetColumnsByName(lambda colName: "averadgePing[ms]" in colName),
        axis=0
    )

    packetLoss = np.average(
        csv.GetColumnsByName(lambda colName: "packetLoss[%]" in colName),
        axis=0
    )

    if(filterGraphs):
        downloadSpeeds = scipy.signal.medfilt(downloadSpeeds, 3)
        uploadSpeeds = scipy.signal.medfilt(uploadSpeeds, 3)
        pingTimes = scipy.signal.medfilt(pingTimes, 3)
        packetLoss = scipy.signal.medfilt(packetLoss, 3)


    plt.plot(timeStamps, downloadSpeeds, 'b')
    plt.plot(timeStamps, uploadSpeeds, 'g')
    plt.plot(timeStamps, pingTimes, 'y')
    plt.plot(timeStamps, packetLoss, 'r')
    plt.show()


if __name__ == '__main__':
    main()
