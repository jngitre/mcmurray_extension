import pandas as pd
import os

CORPUS_PATH = os.path.join(os.path.dirname(__file__), '100k_links_b028')

def get_corpus():
	first_df = pd.read_csv(CORPUS_PATH + '_1-20k.csv', usecols=['w1', 'freq'])
	second_df = pd.read_csv(CORPUS_PATH + '_20-40k.csv', usecols=['w1', 'freq'])
	third_df = pd.read_csv(CORPUS_PATH + '_40-60k.csv', usecols=['w1', 'freq'])
	fourth_df = pd.read_csv(CORPUS_PATH + '_60-80k.csv', usecols=['w1', 'freq'])
	fifth_df = pd.read_csv(CORPUS_PATH + '_80-100k.csv', usecols=['w1', 'freq'])

	whole_corpus = pd.concat([first_df, second_df, third_df, fourth_df, fifth_df])
	return whole_corpus

def main():
	print (get_corpus().head())

if __name__ == '__main__':
	main()
