# Copyright 2018 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import datetime
import unittest

from soundwave import tables


class TestTimeSeries(unittest.TestCase):
  def testDataFrameFromJson(self):
    data = {
        'test_path': (
            'ChromiumPerf/android-nexus5/loading.mobile'
            '/timeToFirstInteractive/Google'),
        'timeseries': [
            ['revision', 'value', 'timestamp', 'r_commit_pos', 'r_chromium'],
            [547397, 2300.3, '2018-04-01T14:16:32.000', '547397', 'adb123'],
            [547398, 2750.9, '2018-04-01T18:24:04.000', '547398', 'cde456'],
            [547423, 2342.2, '2018-04-02T02:19:00.000', '547423', 'fab789']
        ]
    }

    timeseries = tables.timeseries.DataFrameFromJson(data)
    self.assertEqual(len(timeseries), 3)

    # Check values on the first point of the series.
    point = timeseries.reset_index().iloc[0]
    self.assertEqual(point['test_suite'], 'loading.mobile')
    self.assertEqual(point['measurement'], 'timeToFirstInteractive')
    self.assertEqual(point['bot'], 'ChromiumPerf/android-nexus5')
    self.assertEqual(point['test_case'], 'Google')
    self.assertEqual(point['point_id'], 547397)
    self.assertEqual(point['value'], 2300.3)
    self.assertEqual(point['timestamp'], datetime.datetime(
        year=2018, month=4, day=1, hour=14, minute=16, second=32))
    self.assertEqual(point['commit_pos'], 547397)
    self.assertEqual(point['chromium_rev'], 'adb123')
    self.assertEqual(point['clank_rev'], None)


if __name__ == '__main__':
  unittest.main()
