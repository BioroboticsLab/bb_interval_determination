import json
import logging
import os

import cv2

import bb_videos_archiv.core as va_core
import video_reader as vr

ROOT_OUT = './Cam_23'
YEAR = '2016'
PATH = './06_Cam_23_intervals_pair.json'
LOG_PATH = 'log_23.txt'

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')


with open(PATH) as data_file:
    intervals = json.load(data_file)

out_year = os.path.join(ROOT_OUT, YEAR)
if not os.path.exists(out_year):
    os.makedirs(out_year)

va = va_core.Video_Archiv(YEAR)

for interval in intervals:
    out_interval_id = os.path.join(out_year, str(interval['id']).zfill(2))
    if not os.path.exists(out_interval_id):
        os.mkdir(out_interval_id)
    for key in ['left', 'right']:
        if interval[key] is None:
            logging.warning('The side {side} of the Interval {id} is None'.format(side=key, id=interval['id']))
            continue

        path_start = va.get_abs_path_by_name(interval[key]['start_video_name'])
        frame_start = vr.get_first_frame(path_start)
        name_start = '{Cam_id_ts}.jpg'.format(Cam_id_ts=interval[key]['start_video_name'].split('--')[0])

        path_end = va.get_abs_path_by_name(interval[key]['end_video_name'])
        frame_end = vr.get_last_frame(path_end)
        name_end = 'Cam_{id}_{ts}.jpg'.format(id=interval[key]['cam_id'],ts=interval[key]['end_video_name'].split('--')[1][:-4])

        out_side = os.path.join(out_interval_id, key)
        if not os.path.exists(out_side):
            os.mkdir(out_side)

        out_path_start = os.path.join(out_side, name_start)
        cv2.imwrite(out_path_start, frame_start)
        logging.info('The first {side} Frame of interval {id} was written to {out}'.format(
            side=key,
            id=interval['id'],
            out=out_path_start))

        out_path_end = os.path.join(out_side, name_end)
        cv2.imwrite(out_path_end, frame_end)
        logging.info('The last {side} Frame of interval {id} was written to {out}'.format(
            side=key,
            id=interval['id'],
            out=out_path_end))

print('done')
