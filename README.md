# ros_utils

## bagreader.py

* load\_bag reads messages from a rosbag and structures them into a nested dictionary based on topic names and message structure.

Result is cached using joblib.

Requires <https://github.com/pumaking/python_utils>.

## util.py

* tonp / toros can be used to convert from ros msgs to numpy arrays and back.
