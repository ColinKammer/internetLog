import os
import time
import datetime

def executeTest(name, command):
    stream = os.popen(command)
    return '//## ' + name + ': ' + command + '\n' + stream.read() + '\n\n'


def main():
    resultFile = 'results.txt'

    result = '//#! Time: '
    result += datetime.datetime.fromtimestamp(time.time()).strftime('%d.%m.%Y %H:%M:%S')
    result += '\n'

    result += executeTest('Speedtest', './speedtest.py --simple')
    result += executeTest('PingFritzbox', 'ping -c 4 192.168.1.1')
    result += executeTest('PingOrRouter', 'ping -c 4 10.30.0.1')
    result += executeTest('PingGoogle', 'ping -c 4 google.de')
    result += executeTest('PingReddit', 'ping -c 4 reddit.com')
    result += executeTest('PingAmazon', 'ping -c 4 amazon.de')
    result += executeTest('PingYoutube', 'ping -c 4 youtube.com')
    result += executeTest('PingFacebook', 'ping -c 4 facebook.de')
    result += executeTest('PingOneOneOneOne', 'ping -c 4 1.1.1.1')
    result += executeTest('PingSteam', 'ping -c 4 steampowered.de')

    file = open(resultFile, 'a') #Just append, Creates file if it doesn't exist
    file.write(result)
    file.close()


if __name__ == '__main__':
    main()
