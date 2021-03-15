#!/usr/bin/env python

import rospy
from rospy_message_converter import json_message_converter

from test_package.msg import CustAggregatedMsg
from test_package.srv import log_rate


# noinspection DuplicatedCode
class LoggerNode:
    def __init__(self):
        rospy.init_node("LoggerNode", anonymous=True)
        self.sub = rospy.Subscriber("/aggregatedTurtle", CustAggregatedMsg, self.appendData)
        self.rate = rospy.Rate(10)
        self.rateSrv = rospy.Service("log_rate", log_rate, self.changeRate)

    def changeRate(self, srv_msg):
        rospy.loginfo("Update rate to %s" % srv_msg.newRate)
        self.rate = rospy.Rate(srv_msg.newRate)
        return 200

    def appendData(self, msg):
        print("Append Data")
        json = json_message_converter.convert_ros_message_to_json(msg)
        rospy.loginfo("File Append: %s" % json)
        with open(
                file="./turtlesim_aggregated.log",
                mode="a",
                newline='\n'
        ) as file:
            file.write(json + '\n')
        self.rate.sleep()


def main():
    LoggerNode()
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()
