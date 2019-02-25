#!/bin/bash

while :
do
  POLL=$(curl -s -k -L http://34.95.95.41 | grep 'My hostname is')
  echo "$(date) $POLL"
  sleep 0.001
done
