import numpy as np

from scipy.spatial.transform import Rotation as R

class BasicAttrDict(dict):
  pass

def tonp(obj, excludes=None):
  if isinstance(obj, list) or isinstance(obj, tuple):
    return np.array([tonp(x) for x in obj])

  if any([isinstance(obj, t) for t in [int, float, str, bytes]]):
    return obj

  if isinstance(obj, np.ndarray):
    return obj

  if hasattr(obj, "__slots__"):
    fields = set(obj.__slots__)
  elif hasattr(obj, "fields") and callable(obj.fields):
    fields = set(obj.fields())
  else:
    fields = set([f for f in dir(obj) if '__' not in f])

  if fields == set(("secs", "nsecs")):
    return obj.to_sec()

  if fields == set('wxyz'):
    qarr = np.array((obj.x, obj.y, obj.z, obj.w))
    if (not np.all(np.isfinite(qarr))) or np.linalg.norm(qarr) < 1e-8:
      # What to return here?
      return R.from_rotvec([np.nan, np.nan, np.nan])

    return R.from_quat([obj.x, obj.y, obj.z, obj.w])

  if fields == set('xyz'):
    return np.array((obj.x, obj.y, obj.z))

  # Remove redundant "pose.pose" and "twist.twist" in Odometry.
  if fields == set(("pose" , "covariance")) or \
     fields == set(("twist", "covariance")):
    field = min(fields - set(['covariance']))
    ret = tonp(getattr(obj, field))
    ret['covariance'] = tonp(obj.covariance)
    ret.covariance = ret['covariance']
    return ret

  ret = BasicAttrDict()
  for field in fields:
    if excludes is not None and field in excludes:
      continue

    ret[field] = tonp(getattr(obj, field), excludes)
    setattr(ret, field, ret[field])

  return ret

def _tovec3(obj):
  from geometry_msgs.msg import Vector3
  return Vector3(obj[0], obj[1], obj[2])

def _toquat(obj):
  from geometry_msgs.msg import Quaternion
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

def ns_join(*names):
  import functools
  import rospy
  return functools.reduce(rospy.names.ns_join, names, "")
