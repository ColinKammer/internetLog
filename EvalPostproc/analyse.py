import datetime

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

import csvTable

TIMESTAMP_FORMAT = '%d.%m.%Y %H:%M:%S'


def averageNonNan(data, axis):
    masked_data = np.ma.masked_array(data, np.isnan(data))
    return np.ma.average(masked_data, axis=axis)


def main():
    filterGraphs = True

    csv = csvTable.readFile('out.csv')

    timeStamps = list(map(
        lambda x: datetime.datetime.strptime(x, TIMESTAMP_FORMAT),
        csv.RowNames)
    )

    downloadSpeeds = csv.GetColumnByName('Speedtest_download[Mbit/s]')
    uploadSpeeds = csv.GetColumnByName('Speedtest_upload[Mbit/s]')

    pingTimes = averageNonNan(
        csv.GetColumnsByName(lambda colName: "averadgePing[ms]" in colName),
        axis=0
    )

    packetLoss = averageNonNan(
        csv.GetColumnsByName(lambda colName: "packetLoss[%]" in colName),
        axis=0
    )

    if(filterGraphs):
        downloadSpeeds = scipy.signal.medfilt(downloadSpeeds, 3)
        uploadSpeeds = scipy.signal.medfilt(uploadSpeeds, 3)
        pingTimes = scipy.signal.medfilt(pingTimes, 3)
        packetLoss = scipy.signal.medfilt(packetLoss, 3)

    plt.plot(timeStamps, downloadSpeeds, 'b', label='downloadSpeed[Mbit/s]')
    plt.plot(timeStamps, uploadSpeeds, 'g', label='uploadSpeed[Mbit/s]')
    plt.plot(timeStamps, pingTimes, 'y', label='averagePing[ms]')
    plt.plot(timeStamps, packetLoss, 'r', label='averagePacketloss[%]')
    plt.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
    main()
