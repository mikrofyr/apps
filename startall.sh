#!/bin/bash

#FIXME: This is a poor check
RET=`ps aux | grep eventsync  | grep -cv grep`
if [ $RET -eq 0 ]; then
  # Go to desired log directory for this app, start using screen
  cd $LOGDIR
  /usr/bin/screen -L -dm -S eventsync ./eventsync/eventsync.py  -y eventsync/config.yaml 
fi
