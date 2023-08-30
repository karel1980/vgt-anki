#!/usr/bin/env python

import shutil
import os
import sys
import genanki
import json
import collections

def create_deck(category):
    return genanki.Deck(
      10001000,
      'Flemish sign language category %s'%category)

def create_model():
    return genanki.Model(
      1607392319,
      'Simple Model',
      fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'Regions'}
      ],
      templates=[
        {
          'name': 'Card 1',
          'qfmt': '{{Question}}<br/>{{Regions}}',
          'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
      ])

def create_note(model, translation, video, regions):
    return genanki.Note(model=model,
       fields=[translation, video, regions])

def read_json(category):
    data = json.load(open("assets/%s/signs.json"%category))
    result = []
    for entry in data['signOverviews']:
        result.append((entry['translations'], entry['video'],entry['regions']))

    return result

def create_anki_package(category):
    deck = create_deck(category)
    model = create_model()

    terms = read_json(category)
    media_files = []

    for translations, video, regions in terms:
        path=('media/%s/'%category) + video[66:]
        media_files.append(path)
        print (media_files)
        shutil.copyfile(path, os.path.basename(path))
        note = create_note(model, ' / '.join(translations), "[sound:%s]"%(os.path.basename(path)), ' / '.join(regions))
        deck.add_note(note)


    duplicates = [item for item, count in collections.Counter(media_files).items() if count > 1]
    if len(duplicates) > 0:
        print("found duplicate filenames: ", duplicates)
        sys.exit(1)

    if len(media_files) >= 1000:
        print("there are 1000 entries, you are probably missing out - check the limit in the download script")

    if not os.path.exists("decks"):
        os.makedirs("decks")
    apkg = 'decks/%s.apkg'%category
    package = genanki.Package(deck)
    package.media_files = media_files
    package.write_to_file(apkg)
    print("wrote %s"%apkg)


if __name__=="__main__":
    category = sys.argv[1]
    create_anki_package(category)
