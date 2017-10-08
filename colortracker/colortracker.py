import cv2
import datetime
import numpy as np

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

        # orange post-it
        lower_orange = np.array([  0,  130,  100])
        upper_orange = np.array([ 25,170,255])
        mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
        res_orange = cv2.bitwise_and(frame,frame, mask= mask_orange)
        cv2.namedWindow('res_orange', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('res_orange', 640, 360 )
        cv2.imshow('res_orange',res_orange)

        # yellow post-it
        lower_yellow = np.array([ 17, 72, 100])
        upper_yellow = np.array([ 37, 112, 255])
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        res_yellow = cv2.bitwise_and(frame,frame, mask= mask_yellow)
        cv2.namedWindow('res_yellow', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('res_yellow', 640, 360 )
        cv2.imshow('res_yellow',res_yellow)

        # pink post-it
        lower_pink = np.array([ 158, 62, 100])
        upper_pink = np.array([ 178, 112, 255])
        mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)
        res_pink = cv2.bitwise_and(frame,frame, mask= mask_pink)
        cv2.namedWindow('res_pink', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('res_pink', 640, 360 )
        cv2.imshow('res_pink',res_pink)


        # green post-it
        lower_green = np.array([  36,  50,100])
        upper_green = np.array([ 56,100,255])
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        res_green = cv2.bitwise_and(frame,frame, mask= mask_green)
        cv2.namedWindow('res_green', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('res_green', 640, 360 )
        cv2.imshow('res_green',res_green)

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
