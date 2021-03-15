#!/usr/bin/env python
import sys
import rospy
from test_package.srv import start_stop

# Sets value but
# Always throws "b'service cannot process request: service handler returned None'"
if __name__ == "__main__":
    if len(sys.argv) > 1:
        isStop = int(sys.argv[1])
        try:
            rospy.wait_for_service("start_stop")
            srv_setter = rospy.ServiceProxy("start_stop", start_stop)
            srv_setter(isStop)
            print("Set stop to %s" % str(isStop == 0))
        except rospy.ServiceException as exc:
            print("Set of stop failed: %s" % exc)
    else:
        print("Enter 0 to stop and any other number to start")
