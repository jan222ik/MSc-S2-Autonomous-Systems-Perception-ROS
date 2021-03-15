#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Color
from turtlesim.msg import Pose

from test_package.msg import CustAggregatedMsg


# noinspection DuplicatedCode
class CollectAndAggregate:
    def __init__(self):
        rospy.init_node("CollectAndAggregate", anonymous=True)
        # Subscribe to all topics of turtle
        self.twistSub = rospy.Subscriber("/turtle1/cmd_vel", Twist, self.onTwistChanged)
        self.colorSub = rospy.Subscriber("/turtle1/color_sensor", Color, self.onColorChanged)
        self.poseSub = rospy.Subscriber("/turtle1/pose", Pose, self.onPoseChanged)

        # Create publisher:
        self.pub = rospy.Publisher('/aggregatedTurtle', CustAggregatedMsg, queue_size=1)
        self.rate = rospy.Rate(10)

        # Placeholder Msg
        self.message = CustAggregatedMsg()
        self.poseSet = False
        self.colorSet = False
        self.twistSet = False

    def onTwistChanged(self, twist):
        self.message.twist = twist
        self.checkAllSet(twist=True)

    def onColorChanged(self, color):
        self.message.color = color
        self.checkAllSet(color=True)

    def onPoseChanged(self, pose):
        self.message.pose = pose
        self.checkAllSet(pose=True)

    def checkAllSet(self, twist=False, color=False, pose=False):
        if ((self.twistSet and twist) or (self.colorSet and color) or (self.poseSet and pose)) or (
                self.twistSet and self.poseSet and self.colorSet):
            # Value updated twice already or all have new value
            self.publish()
            self.twistSet = False
            self.colorSet = False
            self.poseSet = False
        else:
            self.twistSet = self.twistSet or twist
            self.colorSet = self.colorSet or color
            self.poseSet = self.poseSet or pose

    def publish(self):
        rospy.loginfo("Aggregation")
        #  rospy.loginfo("Aggregation: %s" % self.message)
        self.pub.publish(self.message)
        self.rate.sleep()


def main():
    rospy.init_node("CollectAndAggregate", anonymous=True)
    CollectAndAggregate()
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()
