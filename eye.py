#!/usr/bin/python
import sys

import cv2.cv as cv

<<<<<<< HEAD
CAM = 1
=======
CAM = 0
>>>>>>> b528ba7636462539ddefa2297ef51de047e2480e
CROP_X = 0 #0
CROP_Y = 65 #0
CROP_H = 480 #480
CROP_W = 140 #640
<<<<<<< HEAD
BLACK_LEVEL = 220
=======
BLACK_LEVEL = 185 #220
>>>>>>> b528ba7636462539ddefa2297ef51de047e2480e

POINTS = [
          [[ 66,29],[ 54,54],[ 74,54],[ 62,69],[ 52,84],[ 72,84],[ 60,109]],
          [[110,27],[ 99,52],[122,52],[108,67],[ 98,82],[122,80],[108,107]],
          [[158,25],[147,50],[167,50],[154,65],[146,80],[166,80],[155,106]],
          [[206,25],[196,50],[216,50],[206,65],[196,80],[216,80],[206,105]],
          [[253,25],[242,50],[265,50],[252,65],[242,80],[265,80],[250,105]],
          [[282,27]],
          [[ 27,69]]
          ]
SIZE = 6
LIM = 1000

def mouse_callback(event, x, y, flag, param):
    if (event == 1):    # LBUTTON_DOWN
        print "down x: %d, y: %d" %(x,y)
        
    if (event == 4):    # LBUTTON_UP
        print "up x: %d, y: %d" %(x,y)
    return

class eye:
    def __init__(self, cam, show_frame = 0):
        self.capture = cv.CaptureFromCAM(cam)
        self.do_calibrate = 0
        self.do_show = show_frame
        if self.do_show :
            cv.NamedWindow("camera", 1)
        
    def calibrate(self):
        frame = self.get_frame()
        img = cv.CreateImage(cv.GetSize(frame), frame.depth, frame.channels)
        cv.Copy(frame, img)
#        for b in BOXES:
#            cv.Rectangle(img,(b[0][0],b[0][1]),(b[1][0],b[1][1]),(255,0,0))
        for v in POINTS:
            for p in v:
                cv.Circle(img, (p[0], p[1]), 5, (0,0,255), 1, 8)
        if self.do_calibrate == 0:
            cv.NamedWindow("calibrate", 1)
            cv.SetMouseCallback( "calibrate", mouse_callback )
            self.do_calibrate = 1
            
        cv.ShowImage("calibrate", img)
        print POINTS
        return

    def get_frame(self):
        # get frame
        frame = cv.QueryFrame(self.capture)
        # crop frame
        cv.SetImageROI(frame, (CROP_X, CROP_Y, CROP_H, CROP_W))
        raw = cv.CreateImage(cv.GetSize(frame), frame.depth, frame.channels)
        cv.Copy(frame, raw)
        cv.ResetImageROI(frame)
        cv.Smooth(raw, raw, cv.CV_GAUSSIAN, 3, 0)
        # convert the image to grayscale
        grey = cv.CreateImage(cv.GetSize(raw), cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(raw, grey, cv.CV_RGB2GRAY)
        # convert to B&W
        bw = cv.CreateImage(cv.GetSize(grey), cv.IPL_DEPTH_8U, 1)
        cv.Threshold(grey, bw, BLACK_LEVEL, 255, 1)

        return bw


    def count_pixels(self, img, x, y, w, h):
#        cv.Rectangle(img,(x,y),(x+w,y+h),(255,0,0))
        result = 0
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                result += img[yy, xx]
        return result
        
    def parse_digit(self, img, num ):
        digits = {
            '1110111': 0,
            '0010010': 1,
            '1011101': 2,
            '1011011': 3,
            '0111010': 4,
            '1101011': 5,
            '1101111': 6,
            '1010010': 7,
            '1111111': 8,
            '1111011': 9
        }
        c1 = self.count_pixels(img, POINTS[num][0][0]-SIZE/2, POINTS[num][0][1]-SIZE/2, SIZE, SIZE) > LIM and 1 or 0
        c2 = self.count_pixels(img, POINTS[num][1][0]-SIZE/2, POINTS[num][1][1]-SIZE/2, SIZE, SIZE) > LIM and 1 or 0
        c3 = self.count_pixels(img, POINTS[num][2][0]-SIZE/2, POINTS[num][2][1]-SIZE/2, SIZE, SIZE) > LIM and 1 or 0
        c4 = self.count_pixels(img, POINTS[num][3][0]-SIZE/2, POINTS[num][3][1]-SIZE/2, SIZE, SIZE) > LIM and 1 or 0
        c5 = self.count_pixels(img, POINTS[num][4][0]-SIZE/2, POINTS[num][4][1]-SIZE/2, SIZE, SIZE) > LIM and 1 or 0
        c6 = self.count_pixels(img, POINTS[num][5][0]-SIZE/2, POINTS[num][5][1]-SIZE/2, SIZE, SIZE) > LIM and 1 or 0
        c7 = self.count_pixels(img, POINTS[num][6][0]-SIZE/2, POINTS[num][6][1]-SIZE/2, SIZE, SIZE) > LIM and 1 or 0
        
        res = "%d%d%d%d%d%d%d" % (c1, c2, c3, c4, c5, c6, c7)

#        sys.stdout.write(" %d:%s:" % (num,res))
        
        if res in digits:
#            sys.stdout.write("%d;" % digits[res])
            return digits[res]
#        sys.stdout.write("  ;")
        return None
        
    def run(self):
        frame = self.get_frame()
        if self.do_show :
            cv.ShowImage("camera", frame)
        gr = self.count_pixels(frame, POINTS[5][0][0]-SIZE/2, POINTS[5][0][1]-SIZE/2, SIZE, SIZE) > LIM and 1 or 0
        if gr :
            mi =0
            mi = self.count_pixels(frame, POINTS[6][0][0]-SIZE/2, POINTS[6][0][1]-SIZE/2, SIZE, SIZE) > LIM and 1 or 0
            res = 0
            for i in range(0,5):
                y = self.parse_digit(frame, i)
                if y :
                    res = res+y
                if i < 4:
                    res = res * 10
            if mi :
                return -res
            return res
        else :
            return None
        
if __name__ == "__main__":
    e = eye(CAM, show_frame = 1)
    while True:
        m = e.run()
        print m
        c = cv.WaitKey(1000)
#        print c
        if c > 0:
            if c == 27:
                break
            if c == 99:
                e.calibrate()
