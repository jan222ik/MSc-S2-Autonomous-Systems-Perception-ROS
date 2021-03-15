#!/usr/bin/env python
import sys
import rospy
from test_package.srv import log_rate

# Sets value but
# Always throws "b'service cannot process request: service handler returned None'"
if __name__ == "__main__":
    if len(sys.argv) > 1:
        newRate = float(sys.argv[1])
        try:
            rospy.wait_for_service("log_rate")
            srv_setter = rospy.ServiceProxy("log_rate", log_rate)
            srv_setter(newRate)
            print("Rate set to %s" % newRate)
        except rospy.ServiceException as exc:
            print("Set of log rate failed: %s" % exc)
