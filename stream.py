# Adapted from: https://gist.github.com/shihyuan/4d834d429763e953a40c

import time
import urllib2
import sys
import operator
import numpy as np
import cv2
import skimage.measure


N_STREAMS = 2

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


letter = ''
word = ''
init = False
calibration = 0
frame_rate = 2

def checker(new):
    global letter
    if letter != new:
        letter = new
        return new

    return ''


streamstr_lst = ['', '']

while True:
    for i in range(2):
        streamstr_lst[i] += streams[i].read(1024)

    streamstr = streamstr_lst[1]
    start = 0
    for i in range(frame_rate):
        start = streamstr.find('\xff\xd8', start + 1)
        if start == -1:
            break

    end = streamstr.find('\xff\xd9', start)
    
    if start != -1 and end != -1:
        img_raw = streamstr[start:end+2]
        streamstr_lst[i] = streamstr[end+2:]
        frame = cv2.imdecode(np.fromstring(img_raw, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
        
        rthresh = (frame[:,:,0] < 30).astype(np.uint8)
        gthresh = (frame[:,:,1] < 30).astype(np.uint8)
        bthresh = (frame[:,:,2] < 30).astype(np.uint8)
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

        labels, _ = skimage.measure.label(frame[:,:,0], return_num=True)
        uniques, counts = np.unique(labels[1:], return_counts=True)
        label_finger = uniques[np.argmax(counts)] + 1
        x, y = np.where(labels == label_finger)

        if not init:
            calibration = np.min(x)
            init = True

        pos = np.min(x)

        if pos < calibration * 0.9:
            word += checker('r')
        elif pos < calibration * 1.1:
            word += checker('f')
        elif pos < calibration * 1.3:
            word += checker('v')
        elif pos < calibration * 1.5:
            print(word)
            word = ''

        if cv2.waitKey(1) == 27:
            break
