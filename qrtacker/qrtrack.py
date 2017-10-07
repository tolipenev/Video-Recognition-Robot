import zbar

from PIL import Image
import cv2
import time
from math import atan, sqrt

def processQR():
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
    capture = cv2.VideoCapture(0)

    while True:
        # To quit this program press q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Breaks down the video into frames
        ret, frame = capture.read()

        # Converts image to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        qrs = detectImage( gray )

        print getRobotPos( 'Radulescu', qrs )
        highlightQR( frame, qrs )

        # Displays the current frame
        cv2.imshow('Current', frame)

def distance(p0, p1):
    return sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def getRobotPos( name, qrs ):
    for qr in qrs:
        if not qr[0] == name:
            continue

        # angle
        lineCentreTopDouble = qr[1][0]+qr[1][1]
        lineCentreBottomDouble = qr[1][2]+qr[1][3]

        dx, dy =    lineCentreTopDouble[0]-lineCentreBottomDouble[0], lineCentreTopDouble[1]-lineCentreBottomDouble[1]
        theta = atan( dy/dx )

        # centre is just four point average
        x, y =  (lineCentreTopDouble+lineCentreBottomDouble)[0]/2, (lineCentreTopDouble+lineCentreBottomDouble)[1]/2

        size = distance(qr[1][0], qr[1][3])
        return x, y, theta, size

    return None

def highlightQR( frame, qrs):
        if qrs:
            for qr in qrs:
                cv2.line(frame, qr[1][0], qr[1][1],(255,255,0),5)
                cv2.line(frame, qr[1][1], qr[1][2],(255,255,0),5)
                cv2.line(frame, qr[1][2], qr[1][3],(255,255,0),5)
                cv2.line(frame, qr[1][3], qr[1][0],(255,255,0),5)

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,qr[0],(5,50), font, 2,(255,255,255),4)

def detectImage( grayImage ):
        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        image = Image.fromarray(grayImage)
        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())

        # Scans the zbar image.
        scanner = zbar.ImageScanner()
        scanner.scan(zbar_image)

        # # Prints data from image.
        qr_images = []
        for decoded in zbar_image:
            qr_images.append( [decoded.data, decoded.location] )

        return qr_images

if __name__ == "__main__":
    processQR()
