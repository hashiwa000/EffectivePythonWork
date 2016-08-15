#!/bin/bash

PYTHON_PATH=`which python3`

STATE_FILE_NAME='game_state.bin'
STATE_FILE_PATH="./${STATE_FILE_NAME}"

[ -f ${STATE_FILE_PATH} ] && rm -f ${STATE_FILE_PATH}

ls -ltr | grep ${STATE_FILE_NAME}
${PYTHON_PATH} 01.py
ls -ltr | grep ${STATE_FILE_NAME}
${PYTHON_PATH} 02.py
ls -ltr | grep ${STATE_FILE_NAME}
${PYTHON_PATH} 03.py
ls -ltr | grep ${STATE_FILE_NAME}
${PYTHON_PATH} 04.py

