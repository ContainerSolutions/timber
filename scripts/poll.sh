#!/bin/bash

while :
do
  POLL=$(curl -s -k -L 35.189.94.221/frontend | grep frontend)
  echo "$(date) $POLL"
  sleep 0.001
done
