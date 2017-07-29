import enchant
import nltk
from nltk import FreqDist
from enchant.tokenize import get_tokenizer



def autocorrect(word):

	with open('big.txt', 'r') as f:
		st = get_tokenizer("en_US")

		freq_list = FreqDist(i[0] for dank in f for i in st(dank))



	d = enchant.Dict("en_US")
	words = d.suggest(word)

	for word in words:
		print(word + " : " + str(freq_list[word]))


def edit_distance(word1, word2):
	dp = []
	for 


if __name__ == '__main__':
	autocorrect(raw_input('Input a string: '))





