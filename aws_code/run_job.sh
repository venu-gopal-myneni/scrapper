#!/bin/bash

# Exit immediately if a command fails
set -e

# --- CONFIG ---
PROJECT_DIR="/home/ec2-user/nse"
VENV_DIR=".venv"   # or .venv if that's your folder
TODAY=$(date +"%d-%m-%Y")
echo "Today is $TODAY"
CLI_COMMAND="nse --date $TODAY"  # replace with your command

# --- LOG ---
echo "Starting job at $(date)"

# --- NAVIGATE ---
cd "$PROJECT_DIR" || { echo "Failed to cd into $PROJECT_DIR"; exit 1; }

# --- ACTIVATE VENV ---
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
else
    echo "Virtual environment not found!"
    exit 1
fi

# --- RUN COMMAND ---
echo "Running command: $CLI_COMMAND"
$CLI_COMMAND

# --- DEACTIVATE (optional) ---
deactivate

echo "Job completed at $(date)"