#!/bin/bash

# PID of the program, need to be changed whenever program starts
PROGRAM_PID=158213


convert_kb_to_mb() {
    echo "$1 / 1024" | bc
}

# Check if the program is running
while ps -p $PROGRAM_PID > /dev/null; do
    # Get memory (RSS) in KB, CPU usage in %, and CPU time
    PROCESS_STATS=$(ps -p $PROGRAM_PID -o rss=,%cpu=,etime=)

    # Parse the output to get individual values
    MEM_USAGE_KB=$(echo $PROCESS_STATS | awk '{print $1}')
    CPU_USAGE_PERCENT=$(echo $PROCESS_STATS | awk '{print $2}')
    CPU_TIME=$(echo $PROCESS_STATS | awk '{print $3}')

    MEM_USAGE_MB=$(convert_kb_to_mb $MEM_USAGE_KB)

    # Log 
    echo "Memory: ${MEM_USAGE_MB} MB, CPU Usage: ${CPU_USAGE_PERCENT}%, CPU Time: $CPU_TIME" >> process_log.txt


    sleep 1
done

echo "Program with PID $PROGRAM_PID has stopped running!"
