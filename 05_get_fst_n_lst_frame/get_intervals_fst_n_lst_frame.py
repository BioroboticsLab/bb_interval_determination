u"""Besorgt den ersten und letzten Frame eines Intervalls.

Diese Script wird auf dem Flip ausgeführt und benötigt, die folgenden
.json-Files, diese halten die Intervalle in welchen das Kamerasetup weitestgehend
stabil blieb:
    derived_data/03_ecc_similarity_per_video/Cam_0_intervals_ecc.json
    derived_data/03_ecc_similarity_per_video/Cam_1_intervals_ecc.json
    derived_data/03_ecc_similarity_per_video/Cam_2_intervals_ecc.json
    derived_data/03_ecc_similarity_per_video/Cam_3_intervals_ecc.json
"""
import json
import logging
import os

import cv2

import bb_videos_iterator.video_archiv as va
import video_reader as vr

logging.basicConfig(
    filename='log.txt',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')

varchiv = va.Video_Archiv('2016')
for i in range(4):
    logging.info('Start with camera Cam_{id}'.format(id=i))
    dir_path = './Cam_{id}'.format(id=i)
    if not os.path.exists(dir_path):
        logging.info('Create dir {dir_path}'.format(dir_path=dir_path))
        os.makedirs(dir_path)

    with open("Cam_{id}_intervals_ecc.json".format(id=i), 'r') as jsonfile:

        json_intervals = json.load(jsonfile)

        for row in json_intervals:

            # get first frame in interavl
            path_start = varchiv.get_abs_path_by_name(row['start_video_name'])
            frame_start = vr.get_first_frame(path_start)
            name_start = '{num:02}_fst_{basename}.jpg'.format(
                num=row['id'],
                basename=os.path.splitext(row['start_video_name'])[0])
            out_path_start = os.path.join(dir_path, name_start)
            cv2.imwrite(out_path_start, frame_start)
            logging.info(
                'First Frame was written to {out}'.format(out=out_path_start))

            # get last frame in interval
            path_end = varchiv.get_abs_path_by_name(row['end_safe_video_name'])
            frame_end = vr.get_last_frame(path_end)
            name_end = '{num:02}_lst_{basename}.jpg'.format(
                num=row['id'],
                basename=os.path.splitext(row['end_safe_video_name'])[0])
            out_path_end = os.path.join(dir_path, name_end)
            cv2.imwrite(out_path_end, frame_end)
            logging.info(
                'Last Frame was written to {out}'.format(out=out_path_start))
