import os, csv

CRISISNLP_FOLDER = os.path.join('data', 'CrisisNLP_labeled_data_crowdflower')
OUTPUT_FILE = os.path.join('data', 'crisisnlp_needs.tsv')

with open(OUTPUT_FILE, 'w') as o:
	writer = csv.DictWriter(o, delimiter = '\t',
				fieldnames = ['event', 'tweet_id', 'tweet_text'])
	writer.writeheader()
	
	for folder in os.listdir(CRISISNLP_FOLDER):
		if folder.startswith('20'):
			file = [file for file in os.listdir(os.path.join(CRISISNLP_FOLDER, folder)) 
						if file.endswith('.tsv')][0]
			
			with open(os.path.join(CRISISNLP_FOLDER, folder, file), 'r') as f:
				reader = csv.DictReader(f, delimiter = '\t')
				for row in reader:
					if row['label'] == 'donation_needs_or_offers_or_volunteering_services':
						row['event'] = folder
						del row['label']
						writer.writerow(row)
					