#!/bin/bash            

sudo ydotoold \
    -p /tmp/.ydotool_socket \
    -P 0660 \
    -o "$(id -u):$(id -g)"
