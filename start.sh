#!/bin/bash

echo "Starting MLB Stat Projector..."

cd /Users/noahhooks/Documents/py/forgeproject/backend
/Users/noahhooks/Documents/py/forgeproject/mlb_env/bin/python server.py &
BACKEND_PID=$!
echo "Backend server started (PID: $BACKEND_PID)"

cd /Users/noahhooks/Documents/py/forgeproject/frontend
npm start

kill $BACKEND_PID 2>/dev/null
echo "Servers stopped."
