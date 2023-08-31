#!/bin/bash

set -e

./download-all-media.sh

while read category; do
  ./create-anki-package.py --categories $category --regions "Oost-Vlaanderen" "Vlaanderen"
done <categories.txt
