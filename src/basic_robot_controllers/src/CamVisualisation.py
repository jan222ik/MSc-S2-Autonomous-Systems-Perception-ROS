#! /usr/bin/env python

import sys
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


# Mostly Code from http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython
class CameraVisualisation:

    def __init__(self):
        self.imagePub = rospy.Publisher("image_cv", Image)
        self.greyImagePub = rospy.Publisher("image_cv_grey", Image)

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.callback)

    # noinspection PyPep8Naming
    def callback(self, data):
        try:
            imgCV = self.bridge.imgmsg_to_cv2(data, "bgr8")
            imgGreyCV = self.bridge.imgmsg_to_cv2(data, "mono8")

            cv2.imshow("BGR8 Image", imgCV)
            cv2.imshow("Grayscale Image", imgGreyCV)
            cv2.waitKey(3)

            try:
                self.imagePub.publish(self.bridge.cv2_to_imgmsg(imgCV, "bgr8"))
                self.greyImagePub.publish(self.bridge.cv2_to_imgmsg(imgCV, "mono8"))
            except CvBridgeError as e:
                print(e)
        except CvBridgeError as e:
            print(e)


def main(args):
    vis = CameraVisualisation()
    rospy.init_node('camera_visualisation', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
