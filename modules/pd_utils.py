import os

import iso8601
import pandas as pd


def extract_metadata_videoname(basename):
    """Extract the metadata from a video name/path. (2016).

    >>> extract_metadata_basename('Cam_0_2016-07-19T12:41:22.353295Z--2016-07-19T12:47:02.199607Z.mkv')
    cam_id                                     0
    start_ts    2016-07-19 12:41:22.353295+00:00
    end_ts      2016-07-19 12:47:02.199607+00:00
    dtype: object

    >>> extract_metadata_basename('test/Cam_0_2016-07-19T12:41:22.353295Z--2016-07-19T12:47:02.199607Z.mkv')
    cam_id                                     0
    start_ts    2016-07-19 12:41:22.353295+00:00
    end_ts      2016-07-19 12:47:02.199607+00:00
    dtype: object
    """
    # basename could be a path to a bb video file or just the basename.
    # TODO(gitmirgut): Check if in data from 2015 is in the same string format.
    fn_wo_ext = os.path.splitext(os.path.basename(basename))[0]
    id_str, interval_str = fn_wo_ext.split('_')[1:]
    start_str, end_str = interval_str.split('--')
    id_int = int(id_str)
    start_ts = iso8601.parse_date(start_str)
    end_ts = iso8601.parse_date(end_str)
    series = pd.Series([id_int, start_ts, end_ts],
                       index=['cam_id', 'start_ts', 'end_ts'])
    return series
