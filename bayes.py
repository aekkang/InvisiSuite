from enchant.tokenize import get_tokenizer

def get_best():
    with open('big.txt') as f:
        tokens = []
        words = []
        count = 0
        tokenizer = get_tokenizer('en_US')
        for line in f:
            count += 1
            print count
            for token in tokenizer(line):
                # if token not in tokens:
                #     tokens.append(token[0].lower())
                words.append(token[0].lower())
        tokens = list(set(words))
    print 'Saved tokens.'

    d = {words[0]: {}}
    for i in xrange(1, len(words)):
        if words[i] not in d[words[i-1]]:
            d[words[i-1]][words[i]] = 1
        else:
            d[words[i-1]][words[i]] += 1
        if words[i] not in d:
            d[words[i]] = {}
    print 'Made dictionary.'

    best = {}
    for k, v in d.iteritems():
        temp = []
        for i in range(3):
            if v:
                max_key = max(v.iterkeys(), key = (lambda key: v[key]))
                temp.append(max_key) 
                v.pop(max_key, None)
        best[k] = tuple(temp)
    print 'Got best.'

    print 'Saving file.'
    with open('bayes.txt') as f:
        for k, v in best.iteritems():
            f.write(k + ':')
            for i in range(len(v)):
                f.write(v[i])
                if i != len(v) - 1:
                    f.write(',')
            f.write('\n')
    print 'Saved'

def import_bayes():
    bd = {}
    with open('bayes.txt') as f:
        for line in f:
            temp = line.split(':')
            k, v = temp[0], temp[1].strip()
            vs = v.split(',')
            bd[k] = tuple(vs)
    return bd