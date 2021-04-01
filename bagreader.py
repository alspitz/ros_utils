import os

import rosbag

from python_utils.timeseriesu import DataSet
from ros_utils.util import tonp

import joblib

cachedir = os.path.join(os.path.expanduser('~'), '.cache', 'bagreader')
memory = joblib.Memory(cachedir, verbose=0, bytes_limit=500000000)

@memory.cache()
def load_bag(filename, include=None, include_types=None, exclude=None, exclude_types=None):
  if include is None: include = []
  if include_types is None: include_types = []
  if exclude is None: exclude = []
  if exclude_types is None: exclude_types = []

  if isinstance(include, str):
    include = [include]

  if isinstance(exclude, str):
    exclude = [exclude]

  assert not set(include_types).intersection(set(exclude_types))

  print("Reading bag %s..." % filename)
  bag = rosbag.Bag(filename)
  ttt = bag.get_type_and_topic_info()

  topics = []
  for topic, tt in ttt.topics.items():
    msg_type = tt.msg_type

    name_include = any([it in topic for it in include])
    type_include = msg_type in include_types
    name_exclude = any([et in topic for et in exclude])
    type_exclude = msg_type in exclude_types

    if name_exclude or type_exclude:
      continue

    if include or include_types:
      if name_include or type_include:
        topics.append(topic)
    else:
      topics.append(topic)

  data = DataSet()

  # read_messages will read all if topics is [].
  if topics:
    messages = bag.read_messages(topics)
    for topic, msg, msg_t in messages:
      datas = { 'meta_time' : msg_t.to_sec() }
      if hasattr(msg, 'header'):
        datas['time'] = msg.header.stamp.to_sec()
      else:
        datas['time'] = msg_t.to_sec()

      datas.update(**tonp(msg, excludes=['header']))

      data.add_point(topic, ts_metadata=(ttt.topics[topic].msg_type, topic), **datas)
  else:
    print("WARNING: No suitable topics found in", filename)

  data.finalize()
  return data

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("bagfile", type=str)
  args = parser.parse_args()

  data = load_bag(args.bagfile)
  print(data)
