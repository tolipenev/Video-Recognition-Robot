import cv2
import datetime
import numpy as np


def findPostit( hsv_img, limit_low, limit_up, threshold = 1000 ):
        # pink post-it
        #lower_pink = np.array([ 158, 62, 100])
        #upper_pink = np.array([ 178, 112, 255])
        mask = cv2.inRange(hsv_img, np.array(limit_low), np.array(limit_up))
        #res = cv2.bitwise_and(img_orig,img_orig, mask= mask)

        contours,h = cv2.findContours(mask,1,2)
        contour_areas = [(c, cv2.contourArea(c)) for c in contours]
        cnts_filtered = [c for c, area in contour_areas if area > threshold]

        return cnts_filtered

def highlightPostits( frame, contours, line_width = 3, line_color = (255, 255,0) ):
        if len(contours) > 0:
            cv2.drawContours(frame,contours, -1, line_color, line_width)

def process( infile ):

    # Begin capturing video. You can modify what video source to use with VideoCapture's argument. It's currently set
    # to be your webcam.
    capture = cv2.VideoCapture( infile )

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

        pink_cnt   = findPostit( hsv, [158, 62,100], [178,112,255] )
        green_cnt  = findPostit( hsv, [ 36, 50,100], [ 56,100,255] )
        yellow_cnt = findPostit( hsv, [ 17, 72,100], [ 37,112,255] )
        orange_cnt = findPostit( hsv, [  0,130,100], [ 25,170,255] )

        highlightPostits( frame, pink_cnt)
        highlightPostits( frame, green_cnt)
        highlightPostits( frame, yellow_cnt)
        highlightPostits( frame, orange_cnt)

        # Converts image to grayscale.
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #
        # qrs = qrtrack.detectImage( gray )
        # qrtrack.highlightQR( frame, qrs )
        #
        # robotGeo =  qrtrack.getRobotPos( robotname , qrs )
        # if robotGeo:
        #     qrtrack.showRobot( frame, robotGeo)
        #     print "Robot position (x,y,theta,size)=", robotGeo

        # Displays the current frame
        cv2.namedWindow('Current', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Current', 640, 360 )
        cv2.imshow('Current', frame)

    # Release everything if job is finished
    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    infile = "qr_2017-10-07 21:23:52.avi"
    process( infile )
