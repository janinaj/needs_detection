import sys, os, random, csv
from nltk import sent_tokenize
from nltk.tokenize import TweetTokenizer

NEED_TERMS = set(['need', 'needs', 'needed', 'needing'])

if __name__=="__main__":

    INPUT_FILE = sys.argv[1]
    OUTPUT_FILE = sys.argv[2]
    NUM_SENTS = int(sys.argv[3])

    tokenizer = TweetTokenizer()

    need_sents = []
    with open(INPUT_FILE, 'r') as f:
        with open(OUTPUT_FILE, 'w') as o:
            for line in f:
                sentences = sent_tokenize(line)
                for raw_sent in sentences:
                    raw_tokens = tokenizer.tokenize(raw_sent)

                    if len(NEED_TERMS.intersection(raw_tokens)) > 0:
                    	need_sents.append(raw_sent)
    
    sample = random.choices(need_sents, k = NUM_SENTS)
    with open(OUTPUT_FILE, 'w') as o:
    	writer = csv.writer(o)
    	writer.writerow(['id', 'text'])
    	for id_, sentence in enumerate(sample):
    		writer.writerow([id_, sentence])