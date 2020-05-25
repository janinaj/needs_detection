import os, sys, json, time, ahocorasick
from gensim.models import Word2Vec
from nltk import sent_tokenize
from nltk import pos_tag
from nltk.tokenize import TweetTokenizer

NEED_TERMS = ['needs', 'supplies']

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

# find all nouns closest to NEED_TERMS
def get_ranked_needs(emb_model, nouns, output_file, top = 100):
    top_noun_count = 0
    with open(os.path.join(output_file), 'w') as o:
        for (term, score) in emb_model.wv.most_similar(positive = NEED_TERMS, topn = top * 2):
            if term in nouns:
                top_noun_count += 1
                o.write(term + '\n')

                if top_noun_count == top:
                    break

if __name__=="__main__":
    start_time = time.time()

    INPUT_FILE = sys.argv[1]
    OUTPUT_FOLDER = sys.argv[2]
    OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, 'sentences.json')
    NEEDS_FILE = os.path.join(OUTPUT_FOLDER, 'needs.txt')

    PHRASES_FILE = sys.argv[3]
    PHRASE_THRESHOLD = 0.8
    MIN_PHRASE_LENGTH = 2
    MAX_PHRASE_LENGTH = 5

    if len(sys.argv) < 5:
        TOPN = 100

    tokenizer = TweetTokenizer()

    all_phrases, phrase_search = read_phrases(PHRASES_FILE)

    print('Initialization took {} seconds'.format((time.time() - start_time)))

    # read tweets and split into sentences and tokens
    print('Performing phrase annotation and POS tagging...')
    tagging_start_time = time.time()

    all_sents = []
    nouns = set()
    with open(INPUT_FILE, 'r') as f:
        with open(OUTPUT_FILE, 'w') as o:
            for line in f:
                sentences = sent_tokenize(line)
                for raw_sent in sentences:
                    raw_tokens = tokenizer.tokenize(raw_sent)

                    phrase_sent = annotate_phrases(raw_sent, phrase_search)
                    phrase_tokens = tokenizer.tokenize(phrase_sent)

                    pos = pos_tag(raw_tokens)
                    
                    json.dump({
                        'raw_sent' : raw_sent,
                        'raw_tokens' : raw_tokens,
                        'phrase_sent' : phrase_sent,
                        'phrase_tokens' : phrase_tokens,
                        'pos' : pos
                        }, o)
                    o.write('\n')

                    all_sents.append(phrase_tokens)

                    for (word, tag) in pos:
                        if tag in ['NN', 'NNS', 'NNP', 'NNPS']:
                            nouns.add(word.lower())

    for phrase in all_phrases:
        tokens = phrase.split('-')
        final_token = phrase[-1]

        if final_token in nouns:
            nouns.add(phrase)

    print('Tagging took {} seconds'.format((time.time() - tagging_start_time)))

    # generate word embeddings
    print('Generating word embeddings...')
    embedding_start_time = time.time()

    model = Word2Vec(sentences = all_sents)
    model.save(os.path.join(OUTPUT_FOLDER, 'word2vec.model'))
    print('Embedding took {} seconds'.format((time.time() - embedding_start_time)))

    print('Identifying needs and priorities...')
    detection_start_time = time.time()

    get_ranked_needs(model, nouns, NEEDS_FILE, TOPN)
    
    print('Needs detection took {} seconds'.format((time.time() - detection_start_time)))

    print('End: whole process took {} seconds'.format((time.time() - start_time)))