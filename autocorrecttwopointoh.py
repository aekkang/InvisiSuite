import enchant
from nltk import FreqDist
from enchant.tokenize import get_tokenizer

def freq_list(file_name):
    with open(file_name) as f:
        tokenizer = get_tokenizer('en_US')
        freq_list = FreqDist(w[0].lower() for line in f for w in tokenizer(line))
    return freq_list

def freq_list_from_list(lst):
    return FreqDist(w[0].lower() for w in lst)

def export_freq_list(target_file):
    with open ('target_file.txt', 'w') as f:
        for word in freq_list:
            f.write(word + ',' + str(freq_list[word]) + '\n')

def import_freq_list(source_file):
    freq_dict = {}
    with open(source_file) as f:
        for line in f:
            [word, freq] = line.split(',')
            freq_dict[word] = int(freq)
    return freq_dict

if __name__ == '__main__':
    # freq_list = freq_list('big.txt')
    # freq_list = freq_list_from_list(brown.words())
    freq_dict = import_freq_list()
    