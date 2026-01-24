#!/bin/bash

LOG_FILE="geocoding.log"
DB_FILE="businesses.db"

echo "📍 Monitoring Geocoding Progress..."
echo "Press [CTRL+C] to stop monitoring."
echo "==================================="

while true; do
    DATE=$(date '+%H:%M:%S')
    
    # Check if process is running
    # Note: Requires pgrep
    if pgrep -f "fix_locations.py" > /dev/null; then
        STATUS="RUNNING 🟢"
    else
        STATUS="STOPPED 🔴"
    fi
    
    # Get count from DB
    COUNT=$(sqlite3 $DB_FILE "SELECT count(*) FROM businesses WHERE lat != 0.0 AND lat IS NOT NULL;")
    
    # Get last line of log
    LAST_LOG=$(tail -n 1 $LOG_FILE)
    
    echo "[$DATE] Status: $STATUS | Processed: $COUNT"
    echo "   Last Log: $LAST_LOG"
    echo "-----------------------------------"
    
    sleep 300 # 5 minutes
done
