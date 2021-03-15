#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

from test_package.srv import start_stop


# noinspection DuplicatedCode
class TurtleMover:
    def __init__(self):
        rospy.init_node('turtleMover', anonymous=True)
        # turtlename = rospy.get_param('~turtle')
        turtlename = "turtle1"
        self.pub = rospy.Publisher('%s/cmd_vel' % turtlename, Twist, queue_size=1)
        self.rate = rospy.Rate(10)
        self.stop = False
        self.activeSrv = rospy.Service("start_stop", start_stop, self.setStartStop)

    def start(self):
        while not rospy.is_shutdown():
            if not self.stop:
                self.publish()

    def setStartStop(self, isStop):
        self.stop = isStop.startStop == 0
        return 200

    def publish(self):
        twist = Twist()
        twist.linear.x = 1
        twist.angular.z = 2
        rospy.loginfo(twist)
        self.pub.publish(twist)
        self.rate.sleep()


if __name__ == '__main__':
    try:
        TurtleMover().start()
    except rospy.ROSInterruptException:
        pass
