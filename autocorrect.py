import enchant
import nltk
from nltk import FreqDist
from nltk.corpus import brown
from enchant.tokenize import get_tokenizer

def initialize():
    freq_dict = import_freq_list()

def autocorrect(word):
    with open('big.txt', 'r') as f:
        st = get_tokenizer("en_US")

        freq_list = FreqDist(i for i in brown.words())




    d = enchant.Dict("en_US")
    words = d.suggest(word)

    for word in words:
        print(word + " : " + str(freq_dict[word]))


def edit_distance(word1, word2):
    dp = [[0 for x in range(len(word1)+1)] for x in range(len(word2)+1)]
    for let2 in range(len(word2)+1):
        for let1 in range(len(word1)+1):
            if let2==0:
                dp[let2][let1] = let1*2.0
            elif let1==0:
                dp[let2][let1] = let2*2.0
            elif word1[let1-1]==word2[let2-1]:
                dp[let2][let1] = dp[let2-1][let1-1]
            else:
                dp[let2][let1] = min(dp[let2-1][let1] + 1.2, dp[let2][let1-1] + 1.2, dp[let2-1][let1-1] + mistype(word1[let1-1], word2[let2-1]))
    print(dp[len(word2)][len(word1)])

def mistype(str1, str2):
    assoc = [['q','z'], ['v', 'n', 'g', 'h'], ['x', 'd', 'f', 'v'], ['e', 's', 'w', 'r', 'f', 'c', 'x'], ['w', 's', 'd', 'f', 'r'], ['d', 'e', 'r', 't', 'g', 'v', 'c'], ['f', 't', 'h' ,'v', 'b'], ['g', 't', 'y', 'u', 'j', 'n', 'b'], ['u', 'j', 'k', 'l', 'o'], ['u', 'y', 'h', 'n', 'm', 'k'], ['j', 'm', 'u', 'i', 'l', 'o'], ['k', 'i', 'o', 'p', 'm'], ['n', 'j','k', 'l'], ['b', 'h', 'j', 'k', 'm'], ['i', 'k', 'l', 'p'], ['o', 'l'], ['w', 's', 'a'], ['e', 'd', 'f', 'g', 't'], ['q', 'a', 'z', 'x', 'd', 'c', 'e', 'w'], ['r', 'f', 'g', 'h', 'y'], ['y', 'h', 'j', 'k', 'i'], ['c', 'f' ,'g','b'], ['q', 'a', 's', 'd', 'e'], ['z', 'a', 's', 'd', 'c'], ['t', 'g', 'h', 'j', 'u'], ['a','s','x']]
    str1 = str1.lower()
    str2 = str2.lower()
    if str2 in assoc[ord(str1)-97]:
        return 1
    else:
        return 2

if __name__ == '__main__':
    #autocorrect(raw_input('Input a string: '))
    edit_distance(raw_input('Input a string: '), raw_input('Input a string: '))





