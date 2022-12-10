#!/bin/bash

cd /home/pi/internetLog
python createDatapoint.py 127.0.0.1 productionDB InternetLogInsertOnly passWdForInternetLog
