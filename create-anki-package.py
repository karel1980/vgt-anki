#!/usr/bin/env python

import argparse
import models
import hashlib
import shutil
import os
import sys
import genanki
import json
import collections
from datetime import datetime

class Sign:
    def __init__(self, sign_id, regions, gloss_name, translations, video, categories):
        self.sign_id = sign_id
        self.regions = regions
        self.gloss_name = gloss_name
        self.translations = translations
        self.video = video
        self.categories = categories

def create_deck(title):
    id = int(hashlib.md5(title.encode()).hexdigest(), 16) % 10**9
    return genanki.Deck(id, title)

def create_note(model, id, translation, video, categories, regions):
    return genanki.Note(model=model,
       fields=[id, translation, video, categories, regions])

""" returns a dataframe containing all signs over all categories """
def read_entries(categories):
    categories_per_sign = dict()
    
    signs_by_id = dict()
    cats_by_sign_id = dict()

    for cat in categories:
        data = json.load(open("assets/%s/signs.json"%cat))
        cat_list = data['signOverviews']

        if len(cat_list) >= 1000:
            print("This category (%s) has 1000 entries. Check you aren't limited by the page size in the download script"%(cat))

        for sign in data['signOverviews']:
            id = sign['signId']
            signs_by_id[id] = sign
            cats_by_sign_id.setdefault(id, []).append(cat)
    
    return [ create_sign(s, cats_by_sign_id[s['signId']]) for s in signs_by_id.values() ]

def create_sign(sign_data, categories):
    return Sign(sign_data['signId'], sign_data['regions'], sign_data['glossName'], sign_data['translations'], sign_data['video'], categories)

def create_deck_title(categories, regions):
    c_joined = ', '.join(categories)
    r_joined = ', '.join(regions)
    return 'Flemish sign language: %s / %s'%(c_joined, r_joined)

def all_categories():
    return ["Animal", "Appearance", "City", "Colors", "Communication", "Country", "Culture", "Education", "Family", "Food", "Health", "Home", "Law", "Leasure", "NameSign", "Nature", "Numbers", "Personality", "Profession", "Region", "Religion", "Science", "Sexuality", "Society", "Sport", "Technology", "Time", "Transport"]

def create_anki_package(categories, regions, model):
    deck_title = create_deck_title(categories, regions)
    deck = create_deck(deck_title)
    regions = set(regions)

    all_signs = read_entries(all_categories())
    media_files = set()

    matching_signs = list(filter(lambda s: any(region in s.regions for region in regions) and any(cat in s.categories for cat in categories), all_signs))
    
    for sign in matching_signs:
        path=('media/%s/'%sign.categories[0]) + sign.video[66:]
        media_files.add(path)

        shutil.copyfile(path, os.path.basename(path))

        note = create_note(model, str(sign.sign_id), ' / '.join(sign.translations), "[sound:%s]"%(os.path.basename(path)), '/'.join(sign.categories), '/'.join(sign.regions))
        deck.add_note(note)

    if not os.path.exists("decks"):
        os.makedirs("decks")

    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    prefix = 'deck' if len(categories) != 1 else categories[0]
    apkg = 'decks/%s-%s.apkg'%(prefix, timestamp)
    package = genanki.Package(deck)
    package.media_files = list(media_files)
    package.write_to_file(apkg)
    print("wrote %s"%apkg)
    print("result contains %d notes"%(len(matching_signs)))

def read_categories():
    return [l.strip() for l in open('categories.txt').readlines()]

if __name__=="__main__":
    regions=['Vlaanderen','Oost-Vlaanderen','West-Vlaanderen','Vlaams-Brabant','Antwerpen','Limburg','Unknown']
    categories = read_categories()
    
    parser = argparse.ArgumentParser(description = 'create anki package')
    parser.add_argument('--list-categories', action='store_true')
    parser.add_argument('--list-regions', action='store_true')
    parser.add_argument('--regions', action='store', nargs="*", default=['Vlaanderen'], choices=regions)
    parser.add_argument('--categories', action='store', nargs="+", choices=categories)
    parser.add_argument('--word-to-sign', action='store_true', help='default choice if no other type is specified')
    parser.add_argument('--sign-to-word', action='store_true')
    parser.add_argument('--bidirectional', action='store_true', help='short for --word-to-sign AND --sign-to-word')

    args = parser.parse_args(sys.argv[1:])

    if args.list_categories:
        print("Categories:")
        for cat in categories:
            print(' -',cat.strip())
        print()

    if args.list_regions:
        print("Regions:")
        for cat in open('categories.txt').readlines():
            print(' -',cat.strip())
        print()

    if args.categories is None or len(args.categories) == 0:
        print('Please specify at least one category')
        sys.exit(0)

    model = models.WORD_TO_SIGN
    if args.bidirectional:
        model = models.BIDIRECTIONAL
    elif args.word_to_sign and args.sign_to_word:
        model = models.BIDIRECTIONAL
    elif args.sign_to_word:
        model = models.SIGN_TO_WORD
      
    print("Creating package")
    print("Categories:", args.categories)
    print("Regions:", args.regions)
    print("Model:", model.name)

    create_anki_package(args.categories, args.regions, model)
