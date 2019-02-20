#!/bin/bash

while :
do
  POLL=$(curl -s -k -L 35.189.94.221/backend/api/v1/metadata | jq -r .hostname)
  echo "$(date) $POLL"
  sleep 0.001
done
