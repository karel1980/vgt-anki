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

def create_deck(categories, regions):
    c_joined = ', '.join(categories)
    r_joined = ', '.join(regions)

    title = 'Flemish sign language: %s / %s'%(c_joined, r_joined)
    id = int(hashlib.md5(title.encode()).hexdigest(), 16) % 10**9

    return genanki.Deck(id, title)

def create_note(model, translation, video, category, regions):
    return genanki.Note(model=model,
       fields=[translation, video, category, regions])

def read_terms(category):
    data = json.load(open("assets/%s/signs.json"%category))
    result = []
    for entry in data['signOverviews']:
        result.append((entry['translations'], entry['video'],entry['regions']))

    if len(result) >= 1000:
        print("This category (%s) has 1000 entries. Check you aren't limited by the page size in the download script"%(category))

    return result

def create_anki_package(categories, regions, model):
    deck = create_deck(categories, regions)
    regions = set(regions)

    for category in categories:
        terms = read_terms(category)
        media_files = []

        for translations, video, term_regions in terms:
            if any(region in term_regions for region in regions):
                path=('media/%s/'%category) + video[66:]
                media_files.append(path)
                shutil.copyfile(path, os.path.basename(path))
                note = create_note(model, ' / '.join(translations), "[sound:%s]"%(os.path.basename(path)), category, '/'.join(term_regions))
                deck.add_note(note)

    duplicates = [item for item, count in collections.Counter(media_files).items() if count > 1]
    if len(duplicates) > 0:
        print("found duplicate filenames: ", duplicates)
        sys.exit(1)

    if not os.path.exists("decks"):
        os.makedirs("decks")

    apkg = 'decks/%s_in_%s.apkg'%("-".join(categories),"-".join(regions))
    package = genanki.Package(deck)
    package.media_files = media_files
    package.write_to_file(apkg)
    print("wrote %s"%apkg)
    print("result contains %d notes"%(len(media_files)))

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
