# InternetLog - A logging tool for internet availability


## Licence

MIT

Do whatever you want, but it would be nice to name this repo if you are using it in a Project

## Logging Facility
### Dependencies
This Project depends on the speedtest from https://github.com/sivel/speedtest-cli/.
It is your job to download speedtest.py and to store it in the project directory.
But you can use every other tool as well.

### Usage
createDatapoint.sh must be executed regulary (e.g. by a cronjob every 10 min)

#### Add the cronjob
1. bash: crontab -e
2. For createing a sample every 10 minutes:
3. add the following line: */10  *  *   *   *     /home/pi/internetLog/createDatapoint.sh > /dev/null



## Evalution Facility
