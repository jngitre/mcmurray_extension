import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

CORPUS_PATH = os.path.join(os.path.dirname(__file__), '100k_links_b028')
SCRABBLE_DIFFICULTY = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1,  'f': 4, 'g': 2,
					'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1,
					'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4,
					'x': 8, 'y': 4, 'z': 10}

def get_corpus():
	first_df = pd.read_csv(CORPUS_PATH + '_1-20k.csv', usecols=['w1', 'freq'])
	second_df = pd.read_csv(CORPUS_PATH + '_20-40k.csv', usecols=['w1', 'freq'])
	third_df = pd.read_csv(CORPUS_PATH + '_40-60k.csv', usecols=['w1', 'freq'])
	fourth_df = pd.read_csv(CORPUS_PATH + '_60-80k.csv', usecols=['w1', 'freq'])
	fifth_df = pd.read_csv(CORPUS_PATH + '_80-100k.csv', usecols=['w1', 'freq'])

	whole_corpus = pd.concat([first_df, second_df, third_df, fourth_df, fifth_df]).dropna()

	# some minor operations to clean the string data
	whole_corpus['w1'] = whole_corpus['w1'].str.normalize('NFKD')\
		.str.encode('ascii', errors='ignore')\
		.str.decode('utf-8')
	whole_corpus['w1'] = whole_corpus['w1'].str.lower()
	whole_corpus = whole_corpus.loc[whole_corpus['w1'].str.isalpha()]
	whole_corpus['freq'] = np.log(whole_corpus['freq'])
	return whole_corpus

def calculate_features(corpus: pd.DataFrame):
	corpus['length'] = corpus['w1'].str.len()
	corpus['letters'] = corpus['w1'].str.split()
	corpus['scrabble'] = corpus['w1'].apply(lambda x: sum([SCRABBLE_DIFFICULTY[letter] for letter in x]))
	corpus['difficulty'] = (corpus['length'] + corpus['scrabble']) / corpus['freq']
	return corpus

def generate_histograms(corpus: pd.DataFrame):
	len_array = corpus['length'].values
	freq_array = corpus['freq'].values
	scrabble_array = corpus['scrabble'].values
	diff_array = corpus['difficulty'].values

	plt.hist(freq_array, bins=40, range=(0,20))
	plt.xlabel('Word frequency')
	plt.ylabel('Number of words')
	plt.savefig('frequency_distribution.png')
	plt.clf()

	plt.hist(len_array, bins=20, range=(0,20))
	plt.xlabel('Word length')
	plt.ylabel('Number of words')
	plt.savefig('len_distribution.png')
	plt.clf()

	plt.hist(scrabble_array, bins=40, range=(0,40))
	plt.xlabel('Scrabble difficulty')
	plt.ylabel('Number of words')
	plt.savefig('scrabble_distribution.png')
	plt.clf()

	plt.hist(diff_array, bins=30, range=(0,30))
	plt.xlabel('Word difficulty')
	plt.ylabel('Number of words')
	plt.savefig('difficulty_distribution.png')
	plt.clf()

def main():
	raw_corpus = get_corpus()
	corpus = calculate_features(raw_corpus)
	generate_histograms(corpus)

if __name__ == '__main__':
	main()
