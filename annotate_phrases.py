import os, sys

PHRASES_FILE = sys.argv[1] # file containing the multiword phrases
INPUT_FILE = sys.argv[2] # file to be annotated
OUTPUT_FILE = sys.argv[3] # annotated file
THRESHOLD = float(sys.argv[4])

# read phrases
phrases = []
with open(PHRASES_FILE, 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        if float(line[0]) >= THRESHOLD:
            phrases.append(line[1])

#sort phrase so longer phrases are kept together (e.g. disaster relief vs disaster relief fund)
phrases.sort(key = len, reverse = True)


with open(INPUT_FILE, 'r') as f:
    text = f.read().lower()

    for phrase in phrases:
        text = text.replace(phrase, phrase.replace(' ', '-'))

    with open(OUTPUT_FILE, 'w') as o:
        o.write(text)