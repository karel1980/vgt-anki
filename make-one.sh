#!/bin/bash

set -e

#./download-all-media.sh

./create-anki-package.py --categories $(cat categories.txt) --regions "Oost-Vlaanderen" "Vlaanderen" --bidirectional
