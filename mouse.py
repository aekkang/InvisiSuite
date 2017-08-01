
# Adapted from: https://gist.github.com/shihyuan/4d834d429763e953a40c

import math
import time
import urllib2
import sys
import operator
import numpy as np
import cv2
import skimage.measure

N_STREAMS = 1
N_FINGERS = 10 # REMBER TO CHANGE THIS TO THE RIGHT NUMBER OF FINGERS LOL
COOLIO = 10

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

import autocorrect as ac
import stream
from pynput.keyboard import Key, Controller

def main():
    keyboard = Controller()
    freq_list, freq_list_2, best_bayes = ac.initialize()
    count = 0
    prev = ''
    currs = ''
    prev_key = ' '
    key_in = ''
    print 'Done initializing.'

    hosts=["172.20.10.4"]
    assert len(hosts) == N_STREAMS

    ### Start streams.
    streams = []
    for i, host in zip(range(N_STREAMS), hosts):
        # Get host name.
        hoststr = 'http://{}:8080/video'.format(host)
        
        # Open stream.
        print(hoststr)
        stream = urllib2.urlopen(hoststr)
        print('connected')
        streams.append(stream)

        # print('Streaming {}'.format(hoststr))

    ### Parameters.
    init = False
    cooldown = 0
    jerked = 0
    prev_jerked = 0
    rolling_base_lengths = [[] for _ in range(N_FINGERS)]
    rolling_base_widths = [[] for _ in range(N_FINGERS)]
    streamstr_lst = [''] * N_STREAMS
    stable = True
    clicked = False
    word = ''
    visual = True

    # print("Calibrating...")
    # time.sleep(2)

    
    while True:

        ### Read streams.
        for i in range(N_STREAMS):
            streamstr_lst[i] += streams[i].read(1024)

        streamstr = streamstr_lst[0]
        start = streamstr.find('\xff\xd8')
        end = streamstr.find('\xff\xd9', start)
        
        if start != -1 and end != -1:            
            ### Get frame.
            img_raw = streamstr[start:end+2]
            streamstr_lst[0] = streamstr[end+2:]
            frame = cv2.imdecode(np.fromstring(img_raw, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
            # print "AM I HERE1"
            
            ### Threshold the image.
            # Convert BGR to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # define range of blue color in HSV
            lower_blue = np.array([100,50,50])
            upper_blue = np.array([130,255,255])
            # Threshold the HSV image to get only blue colors
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            frame = cv2.bitwise_and(frame,frame, mask=mask)
            frame = cv2.resize(frame, (600, 400))

            # Get thresh into the correct cv2 readable format
            ret,thresh = cv2.threshold(frame, 0, 1, cv2.THRESH_BINARY)
            thresh = cv2.cvtColor(thresh, cv2.COLOR_RGB2GRAY)
            # Find all the contours in the image
            contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # Get the convex hull of all those contours
            # convex_hulls = [cv2.convexHull(c) for c in contours[0]]
            convex_hulls = np.array(contours[0])
            # Find the area of all those convex hulls so we can take the largest
            contour_areas = [cv2.contourArea(c) for c in convex_hulls]
            # Get the indices of the n largest contours. 
            largest_contour_idxes = np.array(contour_areas).argsort()[-N_FINGERS:][::-1]
            # Get the n largest convex hulls
            largest_convex_hulls = [convex_hulls[i] for i in largest_contour_idxes]
            # TODO: Ensure the convex hulls are a minimum area
            # Draw the n largest convex hulls
            cv2.drawContours(frame, largest_convex_hulls, -1, (255, 0, 0), thickness=-1)
            # print "AM I HERE2"
                                             
            # moments = [cv2.moments(c) for c in largest_convex_hulls]
            # centers = [(int(m['m10']/m['m00']), int(m['m01']/m['m00'])) for m in moments if m['m00'] != 0]
            #
            # for c in centers: # Draw the centers
            #     cv2.circle(frame, c, 2, (0, 255, 0))

            ### Get finger tips and lengths.
            finger_tips = []
            finger_lengths = []
            finger_widths = []
            for convex_hull in largest_convex_hulls:
                # Get finger tips.
                y_min_arg = np.argmin(convex_hull[:, 0, 1])
                finger_tips.append(convex_hull[y_min_arg, 0])

                # Get finger lengths.
                max_y = np.max(convex_hull[:, 0, 1])
                min_y = np.min(convex_hull[:, 0, 1])
                finger_lengths.append(max_y - min_y)
                max_x = np.max(convex_hull[:, 0, 0])
                min_x = np.min(convex_hull[:, 0, 0])
                finger_widths.append(max_x)# - min_x)
            finger_lengths = np.array(finger_lengths)
            finger_widths = np.array(finger_widths)
            finger_tips = np.array(finger_tips)
            sort_order = [i[0] for i in sorted(enumerate(finger_tips), key=lambda x: x[1][0])]
            finger_tips = finger_tips[sort_order]
            finger_lengths = finger_lengths[sort_order]
            finger_widths = finger_widths[sort_order]

            ### Adjust base lengths.
            if not init or len(base_lengths) != N_FINGERS:
                base_lengths = finger_lengths
                true_base_lengths = finger_lengths
            elif stable and len(finger_lengths) == N_FINGERS:
                # If we're in the stable state, this is a chance to update the base lengths.
                # Thus add to the rolling base lengths and recalculate new base lengths.
                for i, f in enumerate(finger_lengths):
                    rolling_base_lengths[i].append(f)
                while all(len(r) > 70 for r in rolling_base_lengths):
                    [r.pop(0) for r in rolling_base_lengths]
                if all(len(r) > 0 for r in rolling_base_lengths):
                    base_lengths = [sum(r) * 1.0 / len(r) for r in rolling_base_lengths]
                # base_lengths = true_base_lengths

            if not init or len(base_widths) != N_FINGERS:
                base_widths = finger_widths
                true_base_widths = finger_widths
            elif stable and len(finger_widths) == N_FINGERS:
                # If we're in the stable state, this is a chance to update the base widths.
                # Thus add to the rolling base widths and recalculate new base widths.
                for i, f in enumerate(finger_widths):
                    rolling_base_widths[i].append(f)
                while all(len(r) > 70 for r in rolling_base_widths):
                    [r.pop(0) for r in rolling_base_widths]
                if all(len(r) > 0 for r in rolling_base_widths):
                    base_widths = [sum(r) * 1.0 / len(r) for r in rolling_base_widths]
                # base_widths = true_base_widths

            ### Recalculate prev & curr.
            if not init:
                prev_tip = finger_tips
                init = True
            curr = finger_tips
            deltas = [int(math.sqrt((p[0]-c[0])**2 + (p[1]-c[1])**2)) for p, c in zip(prev_tip, curr)]
            prev_tip = curr

            ### Show interface.
            if visual:
                # print("HEY")
                # print(frame)
                cv2.imshow('invisikeyboard', frame)
                if cv2.waitKey(1) == 27:
                    break

            ### Cooldown.
            if cooldown > 0:
                cooldown -= 1
                # continue


            ### Meat.
            # Determine whether a key was clicked.
            clicked = any([d > 8 for d in deltas])
            stable = np.sum([d < 3 for d in deltas]) >= 9
            if clicked:
                # prev_jerked = jerked
                # print(prev_key)
                for key, value in FINGER2LETTER.iteritems():
                    if value == prev_key:
                        prev_jerked = int(key[0])
                        break
                jerked = np.argmax(deltas)

                # Cooldown cases.
                if cooldown > 3 and prev_jerked == jerked:
                    continue
                elif cooldown > 3:
                    continue

                offset = 0
                if jerked == 4 or jerked == 5: # SPACE CASE
                    pass
                elif finger_lengths[jerked] > base_lengths[jerked] * 1.1:
                    offset = 1
                elif finger_lengths[jerked] < base_lengths[jerked] * 0.6:
                    offset = -1
                # if jerked == 3 or jerked == 6:
                #     change in tip
                if jerked == 3 or jerked == 6:
                    if math.fabs(finger_widths[jerked] - base_widths[jerked]) > 6:
                        offset += 3
                # print "DO I GET HERE?"
                cooldown = COOLIO
                # print jerked, offset, str(float(finger_lengths[jerked]) / base_lengths[jerked])
                jerk_ratio = str(float(finger_lengths[jerked]) / base_lengths[jerked])
                F2Li = '{},{}'.format(jerked, offset)
                if F2Li in FINGER2LETTER:
                    letter = FINGER2LETTER[F2Li]
                    # if letter == ' ':
                    #     print word
                    #     word = ''
                    # else:
                    #     word += letter                               
                    # print(letter)                                                                                                                                             
                    key_in = letter#, jerk_ratio


        # key_in = stream.rengfunc(prev_key)
        # print(key_in)
        if clicked and cooldown == COOLIO:
            print(key_in)
            prev_key = key_in
            currs += str(key_in)
            # if key_in != '':
            #     keyboard.press(key_in)
            #     keyboard.release(key_in)
            if key_in == ' ':
                currs = currs[:-1]
                # for _ in xrange(count + 1):
                #     keyboard.press(Key.backspace)
                #     keyboard.release(Key.backspace)
                # print("FUIC")
                # print(currs)
                if currs.strip() != '':
                    corrected_word = ac.autocorrect(freq_list, freq_list_2, best_bayes, prev, currs)
                else:
                    corrected_word = ''
                print(corrected_word)
                # print("HEI")
                keyboard.type(corrected_word + ' ')
                # print("HEWFOIUHEWF")
                count = 0
                prev = currs
                currs = ''
            else:
                count += 1
            clicked = False

if __name__ == '__main__':
    main()






# def rengfunc(prev_key, hosts=["172.20.10.4"], visual=True):
    
#     while True:
