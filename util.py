import numpy as np

from scipy.spatial.transform import Rotation as R

from geometry_msgs.msg import Quaternion, Vector3

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

def _tovec3(obj):
  return Vector3(obj[0], obj[1], obj[2])

def _toquat(obj):
  q_wlast = obj.as_quat()
  q_ret = Quaternion()
  q_ret.x = q_wlast[0]
  q_ret.y = q_wlast[1]
  q_ret.z = q_wlast[2]
  q_ret.w = q_wlast[3]
  return q_ret

def toros(obj):
  if type(obj) is R:
    return _toquat(obj)
  elif len(obj.shape) == 1:
    if len(obj) == 3:
      return _tovec3(obj)
  elif len(obj.shape) == 2:
    if obj.shape[1] == 3:
      return [_tovec3(x) for x in obj]

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

