import autocorrect as ac
import stream
from pynput.keyboard import Key, Controller

def main():
    keyboard = Controller()
    freq_list, freq_list_2, best_bayes = ac.initialize()
    count = 0
    prev = ''
    curr = ''
    prev_key = ' '
    print 'Done initializing.'
    
    while True:
        key_in = stream.rengfunc(prev_key)
        print(key_in)
        prev_key = key_in
        keyboard.press(key_in)
        curr += key_in
        keyboard.release(key_in)
        if key_in == ' ':
            curr = curr[:-1]
            for _ in xrange(count + 1):
                keyboard.press(Key.backspace)
                keyboard.release(Key.backspace)
            if curr.strip() != '':
                corrected_word = ac.autocorrect(freq_list, freq_list_2, best_bayes, prev, curr)
            else:
                corrected_word = ''
            keyboard.type(corrected_word + ' ')
            count = 0
            prev = curr
            curr = ''
        else:
            count += 1

if __name__ == '__main__':
    main()