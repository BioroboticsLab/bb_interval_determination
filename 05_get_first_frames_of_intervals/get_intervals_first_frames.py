import csv
import os

import cv2

import video_reader as vr
import bb_binary.parsing as bbb_p
import bb_videos_iterator.video_archiv as va

varchiv = va.Video_Archiv('2016')
for i in range(4):
    with open("intervalls_"+str(i)+".csv", 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for j, row in enumerate(reader):
            path = varchiv.get_abs_path_by_name(row['Start_Video'])
            img = vr.get_first_frame(path)
            name = str(j) + '_' + os.path.splitext(row['Start_Video'])[0] + '.jpg'
            cv2.imwrite(os.path.join('./Cam_'+str(i), name), img)
