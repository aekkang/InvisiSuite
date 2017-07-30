
# U WANT SUM BLUE
def find_blue():
    import cv2
    img = cv2.imread('/home/akang/Documents/projects/invisiboard/testblue.png', 1)
    cv2.imshow('testblue', img)
    print img[5][5]
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def calibrate():
    from stream import rengfunc
    print 'Please type "hello"'
    rengfunc(visual=True)

def main():
    calibrate()

main()