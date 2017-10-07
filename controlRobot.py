from qrtracker import qrtrack
import cv2


def processQR( robotname ):
    """
    A simple function that captures webcam video utilizing OpenCV. The video is then broken down into frames which
    are constantly displayed. The frame is then converted to grayscale for better contrast. Afterwards, the image
    is transformed into a numpy array using PIL. This is needed to create zbar image. This zbar image is then scanned
    utilizing zbar's image scanner and will then print the decodeed message of any QR or bar code. To quit the program,
    press "q".
    :return:
    """

    # Begin capturing video. You can modify what video source to use with VideoCapture's argument. It's currently set
    # to be your webcam.
    capture = cv2.VideoCapture(1)
    capture.set(3, 1920)
    capture.set(4, 1080)
    #capture.set(3, 1280)
    #capture.set(4, 720)

    print "Current resolution:"
    print "- width:", capture.get(3)
    print "- height:", capture.get(4)

    while True:
        # To quit this program press q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Breaks down the video into frames
        ret, frame = capture.read()

        # Converts image to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        qrs = qrtrack.detectImage( gray )
        qrtrack.highlightQR( frame, qrs )

        robotGeo =  qrtrack.getRobotPos( robotname , qrs )
        if robotGeo:
            qrtrack.showRobot( frame, robotGeo)
            print "Robot position (x,y,theta,size)=", robotGeo

        # Displays the current frame
        cv2.namedWindow('Current', cv2.WINDOW_NORMAL)
        cv2.imshow('Current', frame)
        cv2.resizeWindow('Current', 640, 360 )


if __name__ == "__main__":
    processQR( 'Casper Hansen')
