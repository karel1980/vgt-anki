
This project contains scripts to download assets from https://woordenboek.vlaamsegebarentaal.be/ and roll them in an Anki file to help you train your VGT vocabulary.

# What's Anki?

Anki is program to help you learn any topic using flashcard. It's using spaced repetition, which is a fancy way of saying it's good at repeating the hard questions more than the easy ones (https://en.wikipedia.org/wiki/Spaced_repetition)

# What's 'Vlaamse gebarentaal'?

Vlaamse gebarentaal (or VGT for short) is 'Flemish sign language'. It's different from Dutch sign language, and even within VGT there are dialects (but people using different dialects can still communicate).

# Usage

Simply running `./make-all.sh` will produce anki packages in under the 'decks' directory.
Try not to overload website. It's not mine and I don't wish to cause it any harm.
The decks will contain terms for all regions. If you want more control, see Advanced usage below.

## Advanced usage

Using the script `create-anki-package.py` you can have more control over the contents of the created Anki package.

Make sure to download the required categories beforehand using the download scripts `download-media.sh` or `./download-all-media.sh`. Try not to download more than you need.

Using `create-anki-package.py` you can specify which regions to include in a deck, which categories to include in a deck and which card model to use (word to sign, sign to word or bidirectional)

Run `create-anki-package.py -h` for more information.

For example:

    ./create-anki-package.py --regions 'Vlaanderen' 'Oost-Vlaanderen' --categories Numbers Sport --sign-to-word

