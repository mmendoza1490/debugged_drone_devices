#!/usr/bin/bash

bin=".venv/bin/python3"
brk="run.brk"

if [[ -f $brk ]]
then
    echo "there is a debugg process running..."
else
    echo "starting debugged "$(date)  > $brk
    $bin main.py
    rm $brk
fi