#!/bin/bash

set -e

while read category; do
  ./download-media.sh $category
done <categories.txt
