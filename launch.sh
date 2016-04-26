#!/bin/bash
cd ~/Documents/discovery_space_rfid
python scanner.py &
python run.py runserver &
firefox -private-window localhost:5000
