import datetime

import numpy as np
import matplotlib.pyplot as plt

import csvTable

TIMESTAMP_FORMAT = '%d.%m.%Y %H:%M:%S'


def main():
    csv = csvTable.readFile('out.csv')

    timeStamps = list(map(
        lambda x: datetime.datetime.strptime(x, TIMESTAMP_FORMAT),
        csv.RowNames)
    )

    downloadSpeeds = csv.GetColumnByName('Speedtest_download[Mbit/s]')
    uploadSpeeds = csv.GetColumnByName('Speedtest_upload[Mbit/s]')
    
    plt.plot(timeStamps, downloadSpeeds, 'b')
    plt.plot(timeStamps, uploadSpeeds, 'g')
    plt.show()


if __name__ == '__main__':
    main()
