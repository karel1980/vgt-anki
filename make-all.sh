#!/bin/bash

set -e

while read category; do
  ./download-media.sh $category
  ./create-anki-package.py $category
done <categories.txt
