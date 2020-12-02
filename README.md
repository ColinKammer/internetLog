# InternetLog - A logging tool for internet availability


## Licence
MIT

Do whatever you want

It would however be nice to include a link to this project, name it or whatever if you use it.

## Logging Facility
### Dependencies
This Project depends on the speedtest from https://github.com/sivel/speedtest-cli/.
It is your job to download speedtest.py and to store it in the project directory.
But you can use every other tool as well.

### Usage
createDatapoint.sh must be executed regulary (e.g. by a cronjob every 10 min)

#### Add the cronjob
1. bash: crontab -e
2. add the following line: */10 * * * * /home/pi/internetLog/createDatapoint.sh > /dev/null 2>&1 

### Output
The output is the command line output of ping and the speedtest slihtly marked up

#### Syntax
 * //#! Marks the Start of a new Record
 * //## marks the Start of a new Test

## Evalution Facility