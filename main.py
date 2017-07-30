import autocorrect as ac

def main():
    freq_list, freq_list_2, best_bayes = ac.initialize()
    count = 0
    prev = ''
    curr = ''
    'Done initializing.'
    
    while True:
        key_in = rengfunc()
        keyboard.press(key_in)
        curr += key_in
        keyboard.release(key_in)
        if key_in == ' ':
            for _ in xrange(count + 1):
                keyboard.press(Key.backspace)
                keyboard.release(Key.backspace)
            corrected_word = #### AUTOCORRECT BS #### autocorrect(curr[:-1])
            keyboard.type(corrected_word + ' ')
            count = 0
            prev = curr
            curr = ''
        else:
            count += 1

if __name__ == '__main__':
    main()