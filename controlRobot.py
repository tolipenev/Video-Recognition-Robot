from qrtracker import qrtrack
import cv2
import datetime
from colortracker import colortracker

def process( robotname, outputfile ):
    # Begin capturing video. You can modify what video source to use with VideoCapture's argument. It's currently set
    # to be your webcam.
    capture = cv2.VideoCapture(1)
    resolution = (1920,1080)
    #resolution = (1280, 720)
    capture.set(3, resolution[0])
    capture.set(4, resolution[1])

    # Define the codec and create VideoWriter object
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    out = cv2.VideoWriter( outputfile ,fourcc, 20.0, resolution)

    print "saving to file", outputfile

    print "Current resolution:"
    print "- width:", capture.get(3)
    print "- height:", capture.get(4)

    while capture.isOpened():
        # To quit this program press q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Breaks down the video into frames
        ret, frame = capture.read()

        # write the flipped frame
        out.write(frame)

        # Converts image to grayscale.
#        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        pink_cnt   = colortracker.findPostit( hsv, colortracker.hsv_limits['pink'] )
        green_cnt  = colortracker.findPostit( hsv, colortracker.hsv_limits['green'] )
        yellow_cnt = colortracker.findPostit( hsv, colortracker.hsv_limits['yellow'] )
        orange_cnt = colortracker.findPostit( hsv, colortracker.hsv_limits['orange'] )
        blue_cnt   = colortracker.findPostit( hsv, colortracker.hsv_limits['blue'] )

        colortracker.highlightPostits( frame, pink_cnt)
        colortracker.highlightPostits( frame, green_cnt)
        colortracker.highlightPostits( frame, yellow_cnt)
        colortracker.highlightPostits( frame, orange_cnt)
        colortracker.highlightPostits( frame, blue_cnt)

        # robotGeo =  qrtrack.getRobotPos( robotname , qrs )
        # if robotGeo:
        #     qrtrack.showRobot( frame, robotGeo)
        #     print "Robot position (x,y,theta,size)=", robotGeo

        # Displays the current frame
        cv2.namedWindow('Current', cv2.WINDOW_NORMAL)
        cv2.imshow('Current', frame)
        cv2.resizeWindow('Current', 640, 360 )

    # Release everything if job is finished
    capture.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    outfile = "qr_"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+".avi"
    process( 'Casper Hansen', outfile )
