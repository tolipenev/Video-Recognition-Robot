import cv2
import datetime
import numpy as np
import sys
from math import atan2

sys.path.append( '..')
from qrtracker import qrtrack

hsv_limits = {  'pink':   ([158, 62,100], [178,112,255]),
                'green':  ([ 36, 50,100], [ 56,100,255]),
                'yellow': ([ 17, 72,100], [ 37,112,255]),
                'orange': ([  0,130,100], [ 25,170,255]),
                'blue':   ([ 87,150,100], [107,255,255]) }

def findPostit( hsv_img, limits, threshold = 1000 ):
        limit_low, limit_up = limits
        mask = cv2.inRange(hsv_img, np.array(limit_low), np.array(limit_up))

        contours,h = cv2.findContours(mask,1,2)
        contour_areas = [(c, cv2.contourArea(c)) for c in contours]
        cnts_filtered = [c for c, area in contour_areas if area > threshold]

        return cnts_filtered

def highlightPostits( frame, contours, line_width = 3, line_color = (255, 255,0) ):
        if len(contours) > 0:
            cv2.drawContours(frame,contours, -1, line_color, line_width)

def getRobotPos( cnt_front, cnt_back ):
    if len(cnt_front) < 1 or len(cnt_back) < 1:
        return None

    Mf = cv2.moments( cnt_front[0])
    Mb = cv2.moments( cnt_back[0])

    Cf = (int(Mf['m10']/Mf['m00']), int(Mf['m01']/Mf['m00']))
    Cb = (int(Mb['m10']/Mb['m00']), int(Mb['m01']/Mb['m00']))

    x, y = ((Cf[0]+Cb[0])/2, (Cf[1]+Cb[1])/2)
    dx, dy = ((Cf[0]-Cb[0])/2, (Cf[1]-Cb[1])/2)
    theta = atan2( dy, dx )
    size = qrtrack.distance( Cf, Cb)*2

    return x, y, theta, size

def process( infile ):

    # Begin capturing video. You can modify what video source to use with VideoCapture's argument. It's currently set
    # to be your webcam.
    capture = cv2.VideoCapture( infile )
    robotGeoNew = None
    robotGeoCurrent = None

    print "Current resolution:"
    print "- width:", capture.get(3)
    print "- height:", capture.get(4)

    while True:
        # To quit this program press q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Breaks down the video into frames
        ret, frame = capture.read()

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        pink_cnt   = findPostit( hsv, hsv_limits['pink'] )
        green_cnt  = findPostit( hsv, hsv_limits['green'] )
        yellow_cnt = findPostit( hsv, hsv_limits['yellow'] )
        orange_cnt = findPostit( hsv, hsv_limits['orange'] )
        blue_cnt = findPostit( hsv, hsv_limits['blue'] )

        print "count: pink", len(pink_cnt), "green", len(green_cnt)
        robotGeoNew = getRobotPos( green_cnt, pink_cnt)

        highlightPostits( frame, pink_cnt)
        highlightPostits( frame, green_cnt)
        highlightPostits( frame, yellow_cnt)
        highlightPostits( frame, orange_cnt)
        highlightPostits( frame, blue_cnt)

        if not robotGeoCurrent:
            robotGeoCurrent = robotGeoNew
        else:
            new_xy = robotGeoNew[0], robotGeoNew[1]
            current_xy = robotGeoCurrent[0], robotGeoCurrent[1]
            if qrtrack.distance( new_xy, current_xy) < 150:
                robotGeoCurrent = robotGeoNew
            else:
                print "Warning tracking issues..."

        qrtrack.showRobot( frame, robotGeoCurrent)

        # Displays the current frame
        cv2.namedWindow('Current', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Current', 640, 360 )
        cv2.imshow('Current', frame)

    # Release everything if job is finished
    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    #infile = "qr_2017-10-07 21:23:52.avi"
    infile = "qr_2017-10-08 12:55:36.avi"
    process( infile )
