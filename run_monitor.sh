#!/bin/bash

# Change to the script directory
cd "$(dirname "$0")"

# Activate virtual environment (update the path if your venv is elsewhere)
source venv/bin/activate

# Run the monitor script in the background
nohup python site_monitor.py > monitor.log 2>&1 &

# Get the process ID and print confirmation
PID=$!
echo "Site monitor started with PID: $PID"
echo "Output is being logged to monitor.log"
