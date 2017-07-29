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
	dp = [[0 for x in range(len(word1)+1)] for x in range(len(word2)+1)]
	for let2 in range(len(word2)+1):
		for let1 in range(len(word1)+1):
			if let2==0:
				dp[let2][let1] = let1
			elif let1==0:
				dp[let2][let1] = let2
			elif word1[let1-1]==word2[let2-1]:
				dp[let2][let1] = dp[let2-1][let1-1]
			else:
				dp[let2][let1] = min(dp[let2-1][let1] + 1, dp[let2][let1-1] + 1, dp[let2-1][let1-1] + 1)
	print(dp[len(word2)][len(word1)])


if __name__ == '__main__':
	#autocorrect(raw_input('Input a string: '))
	edit_distance(raw_input('Input a string: '), raw_input('Input a string: '))





