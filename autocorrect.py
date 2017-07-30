import enchant
import nltk
import unicodedata
import bayes

from nltk import FreqDist
from nltk.corpus import brown
from nltk.corpus import twitter_samples
from enchant.tokenize import get_tokenizer






#Initializes the frequency distribution for nltk.corpus.brown
def initialize():
    #freq_dict = import_freq_list()
    return (FreqDist(i.lower() for i in brown.words()), FreqDist(i.lower() for dank in twitter_samples.strings() for i in unicodedata.normalize('NFKD', dank).encode('ascii','ignore')), bayes.import_bayes())




#Modify later to read stream and run autocorrect
def tester():
    litty = initialize()
    freq_list = litty[0]
    freq_list2 = litty[1] 
    bayes_dict = litty[2]

    testing_set = [('raning','raining'), ('rainning', 'raining'), ('writtings', 'writings'), ('loking', 'looking'), ('imature', 'immature'), ('haning', 'hanging'), ('furr', 'fur'), ('sxold', 'scold'), ('bacin', 'bacon'), ('thunder', 'thounder'), ('saled', 'sailed'), ('saild', 'sailed'), ('heroe', 'hero'), ('reporter', 'repoter'), ('heer', 'here')]
    cor = 0.0
    tot = 0.0
    for tup in testing_set:
        if tup[1] in autocorrect(freq_list, freq_list, bayes_dict, "", tup[0]):
            cor += 1
        tot += 1
    print(cor/tot)




#Modification of tester method that handles streams
def streamer():

    print('Initializing...')

    pwl = enchant.request_pwl_dict("enchant_pwl.txt")

    #Initialize the two frequency lists
    litty = initialize()
    freq_list = litty[0]
    freq_list2 = litty[1] 
    bayes_dict = litty[2]

    curr = ""
    prev = ""


    while(True):
        letty = raw_input('Letter?  ')
        if letty == ' ' or letty == '':
            print(autocorrect(freq_list, freq_list2, bayes_dict, prev, curr))
            prev = curr
            curr = ""

        else:
            curr += letty





def autocorrect(freq_list, freq_list2, bayes_dict, prev, word):
    d = enchant.Dict("en_US")
    words = d.suggest(word)
    for i in xrange(len(words)):
        words[i] = words[i].lower()


    if word not in words:
        words.append(word)

    scores = list()


    for wordle in words:
        scores.append([wordle,(freq_list[wordle]+freq_list2[wordle])**0.7/(edit_distance(word, wordle) + 0.01)**1.8])
        if edit_distance(word, wordle) == 0 :
            scores[len(scores)-1][1] *= 6.0
            
            if d.check(wordle):
                scores[len(scores)-1][1] += 0.5
            else:
                scores[len(scores)-1][1] -= 0.5

        if prev in bayes_dict and wordle in bayes_dict[prev]:
            scores[len(scores)-1][1] *= 10.0

        if wordle == 'docker':
            scores[len(scores)-1][1] += 1000.0

        if wordle == 'greylock':
            scores[len(scores)-1][1] += 150.0

        if wordle == 'hackfest':
            scores[len(scores)-1][1] += 150.0



        
    scores = sorted(scores, key=lambda x: x[1])

    answer = scores[len(scores)-1][0]
    return answer




def edit_distance(word1, word2):
    
    word1 = word1.lower()
    word2 = word2.lower()

    dp = [[0 for x in range(len(word1)+1)] for x in range(len(word2)+1)]
    for let2 in range(len(word2) + 1):
        for let1 in range(len(word1) + 1):
            if let2==0:
                dp[let2][let1] = let1 * 2.0
            elif let1==0:
                dp[let2][let1] = let2 * 2.0
            elif word1[let1-1]==word2[let2-1]:
                dp[let2][let1] = dp[let2 - 1][let1 - 1]
            else:
                dp[let2][let1] = min(dp[let2 - 1][let1] + 1.2, dp[let2][let1 - 1] + 1.5, dp[let2 - 1][let1- 1 ] + mistype(word1[let1 - 1], word2[let2 - 1]))
    return dp[len(word2)][len(word1)]




def mistype(str1, str2):
    assoc = [['q','z'], ['v', 'n', 'g', 'h'], ['x', 'd', 'f', 'v'], ['e', 's', 'w', 'r', 'f', 'c', 'x'], ['w', 's', 'd', 'f', 'r'], ['d', 'e', 'r', 't', 'g', 'v', 'c'], ['f', 't', 'h' ,'v', 'b'], ['g', 't', 'y', 'u', 'j', 'n', 'b'], ['u', 'j', 'k', 'l', 'o'], ['u', 'y', 'h', 'n', 'm', 'k'], ['j', 'm', 'u', 'i', 'l', 'o'], ['k', 'i', 'o', 'p', 'm'], ['n', 'j','k', 'l'], ['b', 'h', 'j', 'k', 'm'], ['i', 'k', 'l', 'p'], ['o', 'l'], ['w', 's', 'a'], ['e', 'd', 'f', 'g', 't'], ['q', 'a', 'z', 'x', 'd', 'c', 'e', 'w'], ['r', 'f', 'g', 'h', 'y'], ['y', 'h', 'j', 'k', 'i'], ['c', 'f' ,'g','b'], ['q', 'a', 's', 'd', 'e'], ['z', 'a', 's', 'd', 'c'], ['t', 'g', 'h', 'j', 'u'], ['a','s','x']]
    str1 = str1.lower()
    str2 = str2.lower()
    if str2 in assoc[ord(str1) - 97]:
        return 1
    else:
        return 2

if __name__ == '__main__':
    #autocorrect(raw_input('Input a string: '))
    #edit_distance(raw_input('Input a string: '), raw_input('Input a string: '))
    streamer()





