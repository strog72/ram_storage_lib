"""
Ram storage lib tests
Authors:
    Alexander Dolgushin <alexdolgus@gmail.com>
"""

import time
import os
import random
import unittest
import json

from ram_storage import set_value, get_value


FILE_STORAGE = os.environ.get('RAM_STORAGE_FILE', '/tmp/snapshot.csv')
SAVE_PERIOD = int(os.environ.get('RAM_STORAGE_SAVE_TIME', 5))


class TestRamStorage(unittest.TestCase):
    def test_set_value(self):
        in_value = 1
        set_value('v1', 1)
        out_value = get_value('v1')
        self.assertEqual(in_value, out_value)

        values = [1, 'string', [1, 2, 3]]
        for v in values:
            key = random.randint(0, 10)
            set_value(key, v)
            out_value = get_value(key)
            self.assertEqual(v, out_value)

    def test_hashable(self):
        self.assertRaises(ValueError, lambda: set_value([1], [1]))

    def test_file_snapshot(self):
        try:
            os.remove(FILE_STORAGE)
        except OSError:
            pass
        key = 'v1'
        value = 1
        set_value(key, value)
        time.sleep(SAVE_PERIOD + 1)

        # check snapshot is exists
        self.assertTrue(os.path.exists(FILE_STORAGE), "File storage does not exists")

        # check snapshot is identical
        f = open(FILE_STORAGE, 'r')
        self.assertDictEqual({key: value}, json.loads(f.read()))
        f.close()

        # check snapshot modification
        value = 2
        data = {key: value}
        f = open(FILE_STORAGE, 'w')
        f.write(json.dumps(data))
        f.close()
        time.sleep(SAVE_PERIOD + 1)
        self.assertEqual(value, get_value(key), "Changes were lost")


if __name__ == '__main__':
    unittest.main()
