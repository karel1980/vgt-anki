#!/bin/bash

set -e

for cat in $(cat categories.txt); do
  ./download-media.sh $cat
done 
