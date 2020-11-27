#!/usr/bin/env bash

set -ex

if [ $# -ne 1 ]
  then
    echo "Usage: $0 /dev/bus/usb/00N"
fi

date
ps auxf
echo ""
lsof +d "$1" || true
lsof -t +d "$1" | xargs kill || true
echo ""
ps auxf
echo ""
