FINGER2LETTER = {
    '0,-1':'z',
    '0,0':'a',
    '0,1':'q',
    '1,-1':'x',
    '1,0':'s',
    '1,1':'w',
    '2,-1':'c',
    '2,0':'d',
    '2,1':'e',
    '3,-1':'v',
    '3,0':'f',
    '3,1':'r',
    '3,2':'b',
    '3,3':'g',
    '3,4':'t',
    '4,0':' ',
    '5,0':' ',
    '6,2':'n',
    '6,3':'h',
    '6,4':'y',
    '6,-1':'m',
    '6,0':'j',
    '6,1':'u',
    '7,0':'k',
    '7,1':'i',
    '8,0':'l',
    '8,1':'o',
    '9,1':'p'
}
LETTER2FINGER = { val: key for key, val in FINGER2LETTER.iteritems() }

# U WANT SUM BLUE
def find_blue():
    import cv2
    img = cv2.imread('/home/akang/Documents/projects/invisiboard/testblue.png', 1)
    cv2.imshow('testblue', img)
    print img[5][5]
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def calibrate():
    import json
    from stream import rengfunc
    DEFAULT_BOTTOM_LINE = 0.6
    DEFAULT_TOP_LINE = 1.1
    
    phrases = [
        "the quick brown fox jumps over the lazy dog",
        "hick dwarves jam blitzing foxy quip",
        "sex prof gives back no quiz with mild joy",
        "a very big box sailed up then whizzed quickly from japan",
        "my girl wove six dozen plaid jackets before she quit",
        "zelda might fix the job growth plans very quickly on monday",
        "the wizard quickly jinxed the gnomes before they vaporized",
        "Quizzical twins proved my hijack bug fix",
    ]
    circle_jerk_cumulative = {}

    for phrase in phrases:
        print 'Please type "' + phrase + '"'

        for i, p in enumerate(phrase.lower()):
            letter, jerk_ratio = rengfunc(visual=True)
            print p[:i + 1]
            finger_id = LETTER2FINGER[letter][0]
            correct_finger_id = LETTER2FINGER[p]
            if finger_id == correct_finger_id:
                if p in circle_jerk_cumulative:
                    circle_jerk_cumulative[p].append(jerk_ratio)
                else:
                    circle_jerk_cumulative[p] = [jerk_ratio]
        
        # Make the circle_jerk golden ratios
        jerk_ratios_per_letter = {}
        for key in circle_jerk_cumulative.keys():
            sample_jerks = circle_jerk_cumulative[key]
            jerk_ratio = sum(sample_jerks) * 1.0 / len(sample_jerks)
            jerk_ratios_per_letter[key] = jerk_ratio
        
        if len(jerk_ratios_per_letter.keys()) <= 26:
            print "Not all letters were found. Continue please."
            continue

        # Build the circle jerk so far.
        circle_jerk = {}
        
        # left pinky
        circle_jerk['0less'] = find_jerk_ratio(jerk_ratios_per_letter, 'a', 'z')
        circle_jerk['0more'] = find_jerk_ratio(jerk_ratios_per_letter, 'a', 'q')
        circle_jerk['1less'] = find_jerk_ratio(jerk_ratios_per_letter, 's', 'x')
        circle_jerk['1more'] = find_jerk_ratio(jerk_ratios_per_letter, 's', 'w')
        circle_jerk['2less'] = find_jerk_ratio(jerk_ratios_per_letter, 'd', 'c')
        circle_jerk['2more'] = find_jerk_ratio(jerk_ratios_per_letter, 'd', 'e')
        circle_jerk['3less'] = (find_jerk_ratio(jerk_ratios_per_letter, 'f', 'v') + find_jerk_ratio(jerk_ratios_per_letter, 'g', 'b') + find_jerk_ratio(jerk_ratios_per_letter, 'f', 'b') + find_jerk_ratio(jerk_ratios_per_letter, 'g', 'v')) / 4.0
        circle_jerk['3more'] = (find_jerk_ratio(jerk_ratios_per_letter, 'f', 'r') + find_jerk_ratio(jerk_ratios_per_letter, 'g', 't') + find_jerk_ratio(jerk_ratios_per_letter, 'f', 't') + find_jerk_ratio(jerk_ratios_per_letter, 'r', 'g')) / 4.0
        circle_jerk['6less'] = (find_jerk_ratio(jerk_ratios_per_letter, 'h', 'n') + find_jerk_ratio(jerk_ratios_per_letter, 'j', 'm') + find_jerk_ratio(jerk_ratios_per_letter, 'h', 'm') + find_jerk_ratio(jerk_ratios_per_letter, 'n', 'j')) / 4.0
        circle_jerk['6more'] = (find_jerk_ratio(jerk_ratios_per_letter, 'h', 'y') + find_jerk_ratio(jerk_ratios_per_letter, 'j', 'u') + find_jerk_ratio(jerk_ratios_per_letter, 'h', 'u') + find_jerk_ratio(jerk_ratios_per_letter, 'y', 'j')) / 4.0
        circle_jerk['7more'] = find_jerk_ratio(jerk_ratios_per_letter, 'k', 'i')
        circle_jerk['8more'] = find_jerk_ratio(jerk_ratios_per_letter, 'l', 'o')

        with open('circle_jerk.json', 'w') as outf:
            json.dump(circle_jerk, outf)

def find_jerk_ratio(jerk_ratios_per_letter, let1, let2):
    return (jerk_ratios_per_letter[let1] + jerk_ratios_per_letter[let2]) / 2.0

def main():
    calibrate()

main()