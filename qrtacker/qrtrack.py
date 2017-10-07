import zbar

from PIL import Image
import cv2
import time

def main():
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

        qrs = scanImage( gray )
        if qrs:
            for qr in qrs:
                print qr
                cv2.line(frame, qr[1][0], qr[1][1],(255,255,0),5)
                cv2.line(frame, qr[1][1], qr[1][2],(255,255,0),5)
                cv2.line(frame, qr[1][2], qr[1][3],(255,255,0),5)
                cv2.line(frame, qr[1][3], qr[1][0],(255,255,0),5)

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,qr[0],(10,500), font, 4,(255,255,255),2)
                #cv2.putText(frame,qr[0],(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)

            #time.sleep(0.5)

        # Displays the current frame
        cv2.imshow('Current', frame)


def scanImage( grayImage ):
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
            #qr_images.append( [decoded.data, (decoded.location[0], decoded.location[1], decoded.location[2], decoded.location[3])]
            # print decoded
            # print "- ", decoded.data
            # print "- ", decoded.type
            # for point in decoded.location:
            #     print "--", point
            #     #print "--", 'x', point.x, 'y', point.y

        return qr_images


        # if zbar_image:
        #     return zbar_image[0]


if __name__ == "__main__":
    main()
