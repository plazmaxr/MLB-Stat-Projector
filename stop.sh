#!/bin/bash

echo "Stopping MLB Stat Projector servers..."

pkill -f "python.*server.py"
pkill -f "react-scripts"
pkill -f "node.*start"

echo "All servers stopped."
