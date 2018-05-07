#!/usr/bin/env bash
echo "Starting the script"
echo "--------"
date
PROJECT_PATH=PATH # Change to full path
cd ${PROJECT_PATH}
/usr/bin/python ${PROJECT_PATH}/src/main.py >> ${PROJECT_PATH}/log.txt
echo "Finishing the script"
echo "-------"
