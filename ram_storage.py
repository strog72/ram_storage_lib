"""
Ram storage lib
Authors:
    Alexander Dolgushin <alexdolgus@gmail.com>
"""

import time
import json
import os
import datetime
import collections
from threading import Thread
from Queue import Queue

SAVE_PERIOD = int(os.environ.get('RAM_STORAGE_SAVE_TIME', 5))
FILE_STORAGE = os.environ.get('RAM_STORAGE_FILE', '/tmp/snapshot.csv')


def listener(queue):
    """
    Worker thread
    Args:
        queue (Queue.Queue):

    Returns:
        None
    """
    last_save_date = datetime.datetime.utcnow()
    if os.path.exists(FILE_STORAGE):
        with open(FILE_STORAGE, 'r') as f:
            try:
                s = json.loads(f.read())
            except ValueError:
                s = {}
            queue.put(s)
    else:
        queue.put({})

    while True:
        now = datetime.datetime.utcnow()
        s = queue.get()
        # load from disk if file was modified
        if os.path.exists(FILE_STORAGE):
            mtime = os.path.getmtime(FILE_STORAGE)
            if datetime.datetime.utcfromtimestamp(mtime) > last_save_date:
                with open(FILE_STORAGE, 'r') as f:
                    s = json.loads(f.read())
                    last_save_date = now
                    # set modified flag
                    os.utime(FILE_STORAGE, (time.mktime(now.timetuple()), time.mktime(now.timetuple())))
        # save to disk
        if (now - last_save_date).total_seconds() >= SAVE_PERIOD:
            with open(FILE_STORAGE, 'w') as f:
                f.write(json.dumps(s))
                last_save_date = now
        queue.put(s)
        time.sleep(1)


def set_value(key, value):
    """
    Set value
    Args:
        key (hashable):
        value (mixed):

    Returns:
        None
    Raises:
        ValueError
    """
    if not isinstance(key, collections.Hashable):
        raise ValueError("Key must be hashable")
    s = queue.get() or {}
    s[key] = value
    queue.put(s)


def get_value(key):
    """
    Get value
    Args:
        key (hashable):

    Returns:
        mixed or None
    """
    s = queue.get() or {}
    result = s.get(key)
    queue.put(s)
    return result


queue = Queue()
ct = Thread(target=listener, args=(queue,))
ct.daemon = True
ct.start()