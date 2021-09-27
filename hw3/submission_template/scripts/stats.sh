#!/bin/bash

export LN_CNT=$(wc -l < $1)

if [ "$LN_CNT" -lt 10000 ]; then
    echo 'File provided as argument must have at least 10000 lines.' > /dev/stderr
    exit 1
fi

echo $LN_CNT
head -n 1 $1
tail -n 10000 $1 | grep "potus" | wc -l
head -n 200 $1 | tail -n 101 | grep "fake" | wc -l
