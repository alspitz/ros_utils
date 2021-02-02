# ros_utils

## bagreader.py

* load\_bag reads messages from a rosbag and structures them into a nested dictionary based on topic names and message structure.

Result is cached using joblib.

Requires <https://github.com/pumaking/python_utils>.

Example Usage:
```python
import matplotlib.pyplot as plt
from ros_utils.bagreader import load_bag

bagfilename = "..."
bag = load_bag(bagfilename, include=["odom"])
plt.plot(bag.odom.times, bag.odom.pose.position[:, 0], label="X Position")
plt.plot(bag.odom.times, bag.odom.pose.position[:, 1], label="Y Position")
plt.plot(bag.odom.times, bag.odom.pose.position[:, 2], label="Z Position")
plt.legend()
plt.show()
```

## util.py

* tonp / toros can be used to convert from ros msgs to numpy arrays and back.
