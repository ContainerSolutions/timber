#!/bin/bash

while :
do
  POLL=$(curl -s -k -L http://front.u1.timber.training.csol.cloud/ | grep -i --context=0 'My hostname is')
  echo "$(date) $POLL"
  sleep 0.5
done
