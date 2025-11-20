#!/bin/bash

# Start MLB Stat Projector
echo "Starting MLB Stat Projector..."

# Start backend server in background
cd /Users/noahhooks/Documents/py/forgeproject/backend
/Users/noahhooks/Documents/py/forgeproject/mlb_env/bin/python server.py &
BACKEND_PID=$!
echo "Backend server started (PID: $BACKEND_PID)"

# Start frontend server
cd /Users/noahhooks/Documents/py/forgeproject/frontend
npm start

# When frontend exits (Ctrl+C), kill backend too
kill $BACKEND_PID 2>/dev/null
echo "Servers stopped."
