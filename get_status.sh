#!/bin/bash
while true; do
  python3 get_status.py || /bin/bash ./get_status.sh
  sleep 20
done
