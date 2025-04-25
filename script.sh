#!/bin/bash

while true; do
	current_time=$(date +"[%d-%m-%Y %H:%M]")
	current_content=$(cat "dyndns.log")
	{ echo "$current_content"; echo "$current_time"; python dyndns.py; } | tail -n 10000 > "dyndns.log"
	sleep 300
done
