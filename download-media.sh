#!/bin/bash

category=${1:-Numbers}

mkdir -p assets/$category
mkdir -p media/$category

curl -g "https://woordenboek.vlaamsegebarentaal.be/api/signs?c=[%22$category%22]&from=0&g=[]&h=[]&l=[]&mode=ANDExact&q=[]&r=[]&size=1000" > assets/$category/signs.json

cat assets/$category/signs.json|jq  '.signOverviews[].video' -r > assets/$category/media-list.txt

while read url; do
    path="media/$category/${url##*protected_media/}"
    mkdir -p "$(dirname $path)"
    curl "$url" -o "$path"
done <assets/$category/media-list.txt


