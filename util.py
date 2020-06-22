import numpy as np

from scipy.spatial.transform import Rotation as R

from geometry_msgs.msg import Quaternion, Vector3

class BasicAttrDict(dict):
  pass

def tonp(obj, excludes=None):
  if isinstance(obj, list) or isinstance(obj, tuple):
    return np.array([tonp(x) for x in obj])

  if any([isinstance(obj, t) for t in [int, float, str]]):
    return obj

  if hasattr(obj, "__slots__"):
    fields = obj.__slots__

    if set(fields) == set(("secs", "nsecs")):
      return obj.to_sec()

    w = 'w' in fields
    x = 'x' in fields
    y = 'y' in fields
    z = 'z' in fields

    if w and x and y and z and len(fields) == 4:
      return R.from_quat([obj.x, obj.y, obj.z, obj.w])

    elif x and y and z and len(fields) == 3:
      return np.array((obj.x, obj.y, obj.z))

    ret = BasicAttrDict()

    for field in fields:
      if excludes is not None and field in excludes:
        continue

      ret[field] = tonp(getattr(obj, field), excludes)
      setattr(ret, field, ret[field])

    return ret

  print(type(obj), obj)
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
