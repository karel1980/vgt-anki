#!/bin/bash

set -e

#./download-all-media.sh

while read category; do
  ./create-anki-package.py --categories $category --regions "Vlaanderen" --bidirectional
done <categories.txt
