import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

CORPUS_PATH = os.path.join(os.path.dirname(__file__), 'resources/100k_links_b028')
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
	len_array = corpus['length'].values * 20
	freq_array = corpus['freq'].values * 20 
	scrabble_array = corpus['scrabble'].values * 10
	diff_array = corpus['difficulty'].values * 20

	plt.hist(freq_array, bins=40, range=(0,400))
	plt.xlabel('Log word frequency')
	plt.ylabel('Number of words')
	plt.savefig('output/frequency_distribution_scaled.png')
	plt.clf()

	plt.hist(len_array, bins=20, range=(0,400))
	plt.xlabel('Word length')
	plt.ylabel('Number of words')
	plt.savefig('output/len_distribution_scaled.png')
	plt.clf()

	plt.hist(scrabble_array, bins=40, range=(0,400))
	plt.xlabel('Scrabble difficulty')
	plt.ylabel('Number of words')
	plt.savefig('output/scrabble_distribution_scaled.png')
	plt.clf()

	plt.hist(diff_array, bins=30, range=(0,400))
	plt.xlabel('Word difficulty')
	plt.ylabel('Number of words')
	plt.savefig('output/difficulty_distribution.png')
	plt.clf()

	# np.random.shuffle(len_array)
	# np.random.shuffle(freq_array)
	# np.random.shuffle(scrabble_array)
	# np.random.shuffle(diff_array)

	return (len_array, freq_array, scrabble_array, diff_array)

# taken and cleaned up from ex2
def run_mcmurray(word_difficulties, difficulty_type, steps):

    learning_curve = []

    for time_step_number in range(steps):
        current_num_words = 0

        for word_difficulty in word_difficulties:
            if time_step_number >= word_difficulty:
            	current_num_words += 1
        learning_curve.append(current_num_words)

    # Here we plot the number of words known over time
    plt.plot(learning_curve)
    plot_filename = 'output/' + difficulty_type + '_explosion_curve_scaled.png'

    plt.xlabel('Time steps')
    plt.ylabel('# of words known')
    plt.savefig(plot_filename)
    plt.clf()

def main():
	raw_corpus = get_corpus()
	corpus = calculate_features(raw_corpus)
	(len_array, freq_array, scrabble_array, diff_array) = generate_histograms(corpus)
	run_mcmurray(diff_array, 'difficulty_equation', 400)
	run_mcmurray(freq_array, 'frequency', 400)
	run_mcmurray(scrabble_array, 'scrabble', 400)
	run_mcmurray(len_array, 'length', 400)

if __name__ == '__main__':
	main()
