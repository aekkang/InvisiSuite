
# Adapted from: https://gist.github.com/shihyuan/4d834d429763e953a40c

import math
import time
import urllib2
import sys
import operator
import numpy as np
import cv2
import skimage.measure

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
import time

def main(host):
    # keyboard = Controller()
    # freq_list, freq_list_2, best_bayes = ac.initialize()
    # count = 0
    # prev = ''
    # currs = ''
    # prev_key = ' '
    # key_in = ''
    # print 'Done initializing.'

    ### Start stream.
    hosturl = 'http://{}:8080/video'.format(host)
    stream = urllib2.urlopen(hosturl)
    print('Streaming {}'.format(hosturl))

    ### Parameters.
    initialized = False
    start_time = time.time()
    # cooldown = 0
    # jerked = 0
    # prev_jerked = 0
    # rolling_base_lengths = [[] for _ in range(N_FINGERS)]
    # rolling_base_widths = [[] for _ in range(N_FINGERS)]
    # stable = True
    # clicked = False
    # word = ''
    # visual = True
    stream_process = ''
    visual = True

    test_squares = [
        ((200, 200), (215, 215)),
        ((250, 230), (265, 245)),
        ((230, 280), (245, 295)),
    ]
        

    
    while True:
        ### Read stream.
        stream_process += stream.read(1024)

        start_pos = stream_process.find('\xff\xd8')
        end_pos = stream_process.find('\xff\xd9', start_pos)
        
        if start_pos != -1 and end_pos != -1:            
            ### Get frame.
            frame_raw = stream_process[start_pos:end_pos+2]
            stream_process = stream_process[end_pos+2:]
            frame = cv2.imdecode(np.fromstring(frame_raw, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
            frame = cv2.resize(frame, (600, 400))
            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            if not initialized:
                for test_square in test_squares:
                    cv2.rectangle(frame, test_square[0], test_square[1], (0, 255, 0))
                if time.time() - start_time > 3:
                    hand_color = [0] * 3
                    for test_square in test_squares:
                        (x1, y1), (x2, y2) = test_square

                        hand_color += np.average(frame_hsv[y1+1:y2, x1+1:x2], axis=(0, 1))
                    hand_color /= len(test_squares)
                    initialized = True
            else:
                ### Threshold the image.
                # Convert BGR to HSV
                # define range of blue color in HSV
                lower_bound = hand_color - np.array([10, 150, 130])
                upper_bound = hand_color + np.array([10, 150, 150])
                # Threshold the HSV image to get only blue colors
                mask = cv2.inRange(frame_hsv, lower_bound, upper_bound)
                frame = cv2.bitwise_and(frame, frame, mask=mask)

                # Get thresh into the correct cv2 readable format
                ret,thresh = cv2.threshold(frame, 0, 1, cv2.THRESH_BINARY)
                thresh = cv2.cvtColor(thresh, cv2.COLOR_RGB2GRAY)
                # Find all the contours in the image
                contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                # Get the convex hull of all those contours
                convex_hulls = [cv2.convexHull(c) for c in contours[0]]
                # convex_hulls = np.array(contours[0])
                # Find the area of all those convex hulls so we can take the largest
                contour_areas = [cv2.contourArea(c) for c in convex_hulls]
                # Get the indices of the n largest contours. 
                largest_contour_idxes = np.array(contour_areas).argsort()[-2:][::-1]
                # Get the n largest convex hulls
                largest_convex_hulls = [convex_hulls[i] for i in largest_contour_idxes[1:]]
                # TODO: Ensure the convex hulls are a minimum area
                # Draw the n largest convex hulls
                cv2.drawContours(frame, largest_convex_hulls, -1, (255, 255, 255), thickness=-1)


            if visual:
                cv2.imshow('invisisuite', frame)
                if cv2.waitKey(1) == 27:
                    break
                                             
            # moments = [cv2.moments(c) for c in largest_convex_hulls]
            # centers = [(int(m['m10']/m['m00']), int(m['m01']/m['m00'])) for m in moments if m['m00'] != 0]

            # ### Get finger tips and lengths.
            # finger_tips = []
            # finger_lengths = []
            # finger_widths = []
            # for convex_hull in largest_convex_hulls:
            #     # Get finger tips.
            #     y_min_arg = np.argmin(convex_hull[:, 0, 1])
            #     finger_tips.append(convex_hull[y_min_arg, 0])

            #     # Get finger lengths.
            #     max_y = np.max(convex_hull[:, 0, 1])
            #     min_y = np.min(convex_hull[:, 0, 1])
            #     finger_lengths.append(max_y - min_y)
            #     max_x = np.max(convex_hull[:, 0, 0])
            #     min_x = np.min(convex_hull[:, 0, 0])
            #     finger_widths.append(max_x)# - min_x)
            # finger_lengths = np.array(finger_lengths)
            # finger_widths = np.array(finger_widths)
            # finger_tips = np.array(finger_tips)
            # sort_order = [i[0] for i in sorted(enumerate(finger_tips), key=lambda x: x[1][0])]
            # finger_tips = finger_tips[sort_order]
            # finger_lengths = finger_lengths[sort_order]
            # finger_widths = finger_widths[sort_order]

            # ### Adjust base lengths.
            # if not init or len(base_lengths) != N_FINGERS:
            #     base_lengths = finger_lengths
            #     true_base_lengths = finger_lengths
            # elif stable and len(finger_lengths) == N_FINGERS:
            #     # If we're in the stable state, this is a chance to update the base lengths.
            #     # Thus add to the rolling base lengths and recalculate new base lengths.
            #     for i, f in enumerate(finger_lengths):
            #         rolling_base_lengths[i].append(f)
            #     while all(len(r) > 70 for r in rolling_base_lengths):
            #         [r.pop(0) for r in rolling_base_lengths]
            #     if all(len(r) > 0 for r in rolling_base_lengths):
            #         base_lengths = [sum(r) * 1.0 / len(r) for r in rolling_base_lengths]
            #     # base_lengths = true_base_lengths

            # if not init or len(base_widths) != N_FINGERS:
            #     base_widths = finger_widths
            #     true_base_widths = finger_widths
            # elif stable and len(finger_widths) == N_FINGERS:
            #     # If we're in the stable state, this is a chance to update the base widths.
            #     # Thus add to the rolling base widths and recalculate new base widths.
            #     for i, f in enumerate(finger_widths):
            #         rolling_base_widths[i].append(f)
            #     while all(len(r) > 70 for r in rolling_base_widths):
            #         [r.pop(0) for r in rolling_base_widths]
            #     if all(len(r) > 0 for r in rolling_base_widths):
            #         base_widths = [sum(r) * 1.0 / len(r) for r in rolling_base_widths]
            #     # base_widths = true_base_widths

            # ### Recalculate prev & curr.
            # if not init:
            #     prev_tip = finger_tips
            #     init = True
            # curr = finger_tips
            # deltas = [int(math.sqrt((p[0]-c[0])**2 + (p[1]-c[1])**2)) for p, c in zip(prev_tip, curr)]
            # prev_tip = curr

            # ### Show interface.
            # if visual:
            #     # print("HEY")
            #     # print(frame)
            #     cv2.imshow('invisikeyboard', frame)
            #     if cv2.waitKey(1) == 27:
            #         break

            # ### Cooldown.
            # if cooldown > 0:
            #     cooldown -= 1
            #     # continue


            # ### Meat.
            # # Determine whether a key was clicked.
            # clicked = any([d > 8 for d in deltas])
            # stable = np.sum([d < 3 for d in deltas]) >= 9
            # if clicked:
            #     # prev_jerked = jerked
            #     # print(prev_key)
            #     for key, value in FINGER2LETTER.iteritems():
            #         if value == prev_key:
            #             prev_jerked = int(key[0])
            #             break
            #     jerked = np.argmax(deltas)

            #     # Cooldown cases.
            #     if cooldown > 3 and prev_jerked == jerked:
            #         continue
            #     elif cooldown > 3:
            #         continue

            #     offset = 0
            #     if jerked == 4 or jerked == 5: # SPACE CASE
            #         pass
            #     elif finger_lengths[jerked] > base_lengths[jerked] * 1.1:
            #         offset = 1
            #     elif finger_lengths[jerked] < base_lengths[jerked] * 0.6:
            #         offset = -1
            #     # if jerked == 3 or jerked == 6:
            #     #     change in tip
            #     if jerked == 3 or jerked == 6:
            #         if math.fabs(finger_widths[jerked] - base_widths[jerked]) > 6:
            #             offset += 3
            #     # print "DO I GET HERE?"
            #     cooldown = COOLIO
            #     # print jerked, offset, str(float(finger_lengths[jerked]) / base_lengths[jerked])
            #     jerk_ratio = str(float(finger_lengths[jerked]) / base_lengths[jerked])
            #     F2Li = '{},{}'.format(jerked, offset)
            #     if F2Li in FINGER2LETTER:
            #         letter = FINGER2LETTER[F2Li]
            #         # if letter == ' ':
            #         #     print word
            #         #     word = ''
            #         # else:
            #         #     word += letter                               
            #         # print(letter)                                                                                                                                             
            #         key_in = letter#, jerk_ratio


        # # key_in = stream.rengfunc(prev_key)
        # # print(key_in)
        # if clicked and cooldown == COOLIO:
        #     print(key_in)
        #     prev_key = key_in
        #     currs += str(key_in)
        #     # if key_in != '':
        #     #     keyboard.press(key_in)
        #     #     keyboard.release(key_in)
        #     if key_in == ' ':
        #         currs = currs[:-1]
        #         # for _ in xrange(count + 1):
        #         #     keyboard.press(Key.backspace)
        #         #     keyboard.release(Key.backspace)
        #         # print("FUIC")
        #         # print(currs)
        #         if currs.strip() != '':
        #             corrected_word = ac.autocorrect(freq_list, freq_list_2, best_bayes, prev, currs)
        #         else:
        #             corrected_word = ''
        #         print(corrected_word)
        #         # print("HEI")
        #         keyboard.type(corrected_word + ' ')
        #         # print("HEWFOIUHEWF")
        #         count = 0
        #         prev = currs
        #         currs = ''
        #     else:
        #         count += 1
        #     clicked = False

if __name__ == '__main__':
    host = sys.argv[1]
    main(host)






# def rengfunc(prev_key, hosts=["172.20.10.4"], visual=True):
    
#     while True:
