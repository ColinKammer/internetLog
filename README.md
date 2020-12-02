# InternetLog - A logging tool for internet availability


## Licence
MIT

Whatever you want

It would be nice to include a link to this project, name it or whatever if you use it.

## Dependencies
This Project usess the speedtest from https://github.com/sivel/speedtest-cli/.
It is your job to download speedtest.py and to store it in the project directory.

## Usage
createDatapoint.sh must be executed regulary (e.g. by a cronjob every 10 min)

### Add the cronjob
bash: crontab -e 
\* add the following line: */10 * * * * /home/pi/internetLog/createDatapoint.sh > /dev/null 2>&1 \*

## Output
The output is the command line output of ping and the speedtest slihtly marked up

### Syntax
\* //#! Marks the Start of a new Record \*
\* //## marks the Start of a new Test \*
