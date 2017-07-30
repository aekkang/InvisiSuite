import autocorrect as ac
import stream

def main():
    freq_list, freq_list_2, best_bayes = ac.initialize()
    count = 0
    prev = ''
    curr = ''
    prev_key = ''
    'Done initializing.'
    
    while True:
        key_in = stream.rengfunc(prev_key)
        prev_key = key_in
        keyboard.press(key_in)
        curr += key_in
        keyboard.release(key_in)
        if key_in == ' ':
            curr = curr[:-1]
            for _ in xrange(count + 1):
                keyboard.press(Key.backspace)
                keyboard.release(Key.backspace)
            corrected_word = ac.autocorrect(freq_list, freq_list_2, best_bayes, prev, curr)
            keyboard.type(corrected_word + ' ')
            count = 0
            prev = curr
            curr = ''
        else:
            count += 1

if __name__ == '__main__':
    main()