import os, sys, json, time, ahocorasick
from gensim.models import Word2Vec
from nltk import sent_tokenize
from nltk import pos_tag
from nltk.chunk import ne_chunk
from stat_parser import Parser
from nltk.tokenize import TweetTokenizer
from collections import defaultdict
from spacy.tokens import Doc

# read phrases file
def read_phrases(PHRASES_FILE):
    # ahocorasick: faster way of searching for phrases in text
    phrase_search = {}
    for i in range(MIN_PHRASE_LENGTH, MAX_PHRASE_LENGTH + 1):
        phrase_search[i] = ahocorasick.Automaton()

    all_phrases = []
    with open(PHRASES_FILE, 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            if float(line[0]) >= PHRASE_THRESHOLD:
                if line[1].endswith("'s"):
                    line[1] = line[1][:-2]
                
                tokens = tokenizer.tokenize(line[1])
                if len(tokens) <= MAX_PHRASE_LENGTH and len(tokens) >= MIN_PHRASE_LENGTH:
                    phrase = '-'.join(tokens)

                    phrase_search[len(tokens)].add_word(line[1], (line[1], phrase))

                    all_phrases.append(phrase)

    for i in range(MIN_PHRASE_LENGTH, MAX_PHRASE_LENGTH + 1):
        phrase_search[i].make_automaton()
                    
    return all_phrases, phrase_search

# annotate phrases in text so they are kept as unigrams
def annotate_phrases(raw_sent, phrases):
    phrase_sent = raw_sent.lower()
    for i in range(MAX_PHRASE_LENGTH , MIN_PHRASE_LENGTH - 1, -1):
        phrases_in_sent = {}
        for end_index, (phrase, combined_phrase) in phrases[i].iter(phrase_sent):
            phrases_in_sent[phrase] = combined_phrase

        for phrase in sorted(phrases_in_sent, key = len, reverse = True):
            phrase_sent = phrase_sent.replace(phrase, phrases_in_sent[phrase])

    return phrase_sent

def get_nouns(vocab_pos, phrases):
    nouns = set()
    for word, tags in vocab_pos.items():
        # if word == 'needed':
        #     print(tags)
        # if word is more frequently used as a noun, add it to list of nouns
        if max(tags, key = tags.get) in ['NN', 'NNS', 'NNP', 'NNPS']:
            nouns.add(word)

    for phrase in phrases:
        tokens = phrase.split('-')
        final_token = tokens[-1]

        if final_token in nouns:
            nouns.add(phrase)

    return nouns

def tweet_tokenizer(text):
    tokens = tokenizer.tokenize(text)

    return Doc(nlp.vocab, tokens)

if __name__=="__main__":
    start_time = time.time()

    INPUT_FILE = sys.argv[1]
    OUTPUT_FOLDER = sys.argv[2]
    OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, 'sentences.json')
    NEEDS_FILE = os.path.join(OUTPUT_FOLDER, 'specific-needs.txt')

    # PHRASES_FILE = sys.argv[3]
    # PHRASE_THRESHOLD = 0.8
    # MIN_PHRASE_LENGTH = 2
    # MAX_PHRASE_LENGTH = 5

    # if len(sys.argv) < 5:
    #     TOPN = 100

    tokenizer = TweetTokenizer()

    nlp = spacy.load('en_core_web_sm')
    nlp.tokenizer = tweet_tokenizer

    # all_phrases, phrase_search = read_phrases(PHRASES_FILE)

    print('Initialization took {} seconds'.format((time.time() - start_time)))

    # read tweets and split into sentences and tokens
    print('Performing phrase annotation and POS tagging...')
    tagging_start_time = time.time()

    all_sents = []
    vocab_pos = {}
    with open(INPUT_FILE, 'r') as f:
        with open(OUTPUT_FILE, 'w') as o:
            for line in f:
                sentences = sent_tokenize(line)
                for raw_sent in sentences:
                    if 'needs' in raw_sent:
                        doc = nlp(raw_sent)

            
    print('END: whole process took {} seconds'.format((time.time() - start_time)))