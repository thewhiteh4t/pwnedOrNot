#!/bin/bash
set -e
if [ "$1" = '' ]; then
   python3 pwnedornot.py -h
fi
exec "$@"
