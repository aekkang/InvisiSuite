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

# Start streams.
streams = []
for i in range(N_STREAMS):
    # Get host name.
    host = sys.argv[i + 1]
    hoststr = 'http://{}:8080/video'.format(host)
    
    # Open stream.
    stream = urllib2.urlopen(hoststr)
    streams.append(stream)

    print('Streaming {}'.format(hoststr))


init = False
calibration = 0
n_frame = 0
n_last = 0

streamstr_lst = ['', '']

while True:
    n_frame += 1
    for i in range(N_STREAMS):
        streamstr_lst[i] += streams[i].read(1024)

    streamstr = streamstr_lst[0]
    start = 0
    # for i in range(frame_rate):
    start = streamstr.find('\xff\xd8')#, start + 1)
    # if start == -1:
    #     break

    end = streamstr.find('\xff\xd9', start)
    
    if start != -1 and end != -1:
        img_raw = streamstr[start:end+2]
        streamstr_lst[0] = streamstr[end+2:]

        frame = cv2.imdecode(np.fromstring(img_raw, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
        
        # Filter for the detected color
        75, 150, 255
        rthresh = (frame[:,:,0] < 100).astype(np.uint8)
        gthresh = (frame[:,:,1] < 200).astype(np.uint8)
        bthresh = (frame[:,:,2] > 200).astype(np.uint8)
        thresh = (rthresh + gthresh + bthresh == 3)
        empty = np.zeros_like(frame[:,:,2])

        frame[:,:,0] = thresh * 255
        frame[:,:,1] = thresh * 255
        frame[:,:,2] = thresh * 255

        frame = cv2.resize(frame, (600, 400))
        cv2.imshow('invisikeyboard', frame)

        # area = np.sum(thresh)
        # if not init:
        #     calibration = area
        #     letter = 'f'
        #     init = True

        labels, _ = skimage.measure.label(thresh, return_num=True)
        uniques, counts = np.unique(labels, return_counts=True)

        if len(counts) > 0:
            label_finger = uniques[np.argmax(counts[1:]) + 1]
        else:
            continue
        x, y = np.where(labels == label_finger)

        # x, y = np.where(frame[:,:,0])

        if not init:
            calibration = np.min(x)
            prev = np.min(y)
            curr = np.min(y)
            init = True

        pos = np.min(x)
        prev = curr
        curr = np.min(y)
        clicked = math.fabs(curr - prev) >= 10

        if pos < calibration * 0.9 and clicked:
            if n_frame - n_last > 200:
                print('r')
                n_last = n_frame
        elif pos < calibration * 1.1 and clicked:
            if n_frame - n_last > 200:
                print('f')
                n_last = n_frame
        elif pos < calibration * 1.3 and clicked:
            if n_frame - n_last > 200:
                print('v')
                n_last = n_frame
        # elif pos < calibration * 1.5:
        #     print(word)
        #     word = ''

        if cv2.waitKey(1) == 27:
            break
