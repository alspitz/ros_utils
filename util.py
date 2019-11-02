import numpy as np

from scipy.spatial.transform import Rotation as R

from geometry_msgs.msg import Vector3

def tonp(obj):
  if isinstance(obj, list) or isinstance(obj, tuple):
    return np.array([tonp(x) for x in obj])

  if isinstance(obj, int) or isinstance(obj, float):
    return obj

  w = hasattr(obj, 'w')
  x = hasattr(obj, 'x')
  y = hasattr(obj, 'y')
  z = hasattr(obj, 'z')

  if w and x and y and z:
    return R.from_quat([obj.x, obj.y, obj.z, obj.w])

  elif x and y and z:
    return np.array((obj.x, obj.y, obj.z))

  print(obj)
  assert False

def toros(obj):
  if len(obj.shape) == 1:
    if len(obj) == 3:
      return Vector3(obj[0], obj[1], obj[2])
  elif len(obj.shape) == 2:
    if obj.shape[1] == 3:
      return [Vector3(x[0], x[1], x[2]) for x in obj]

def odomtostate(odom):
  if hasattr(odom.pose, 'pose'):
    return np.hstack((
      tonp(odom.pose.pose.position),
      tonp(odom.twist.twist.linear),
      tonp(odom.pose.pose.orientation).as_euler('ZYX')[::-1],
      tonp(odom.twist.twist.angular)))
  else:
    # Assume it is OdomNoCov
    return np.hstack((
      tonp(odom.pose.position),
      tonp(odom.twist.linear),
      tonp(odom.pose.orientation).as_euler('ZYX')[::-1],
      tonp(odom.twist.angular)))

