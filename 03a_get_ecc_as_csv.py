# coding: utf-8

# # What?
#
# Stand: 17/06/20
#
# Bestimmung des **ECC** und der **warpmatrix** der ersten frames aufeinanderfolgender Videos.

import csv
import datetime
import glob
import os
import subprocess as sp

import cv2
import iso8601
import numpy as np


class VideoReader:

    def __init__(self, video_path,
                 ffmpeg_stderr_fd=None,
                 format='guess_on_ext',
                 ffmpeg_bin='ffmpeg',
                 ffprobe_bin='ffprobe'):
        if format == 'guess_on_ext':
            format = self.guess_format_on_extension(video_path)

        vidread_command = [
            ffmpeg_bin,
            '-i', video_path,
            '-f', 'image2pipe',
            '-pix_fmt', 'gray',
            '-vsync', '0',
            '-vcodec', 'rawvideo', '-'
        ]

        if format is not None:
            vidread_command.insert(1, '-vcodec')
            vidread_command.insert(2, format)

        resolution_command = [
            ffprobe_bin,
            '-v', 'error',
            '-of', 'flat=s=_',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=height,width',
            video_path
        ]

        pipe = sp.Popen(resolution_command, stdout=sp.PIPE, stderr=sp.PIPE)
        infos = pipe.stdout.readlines()
        self.w, self.h = [int(s.decode('utf-8').strip().split('=')[1]) for s in infos]

        self.video_pipe = sp.Popen(vidread_command,
                                   stdout=sp.PIPE,
                                   stderr=ffmpeg_stderr_fd)
        self.frames = 0

    @staticmethod
    def guess_format_on_extension(video_path):
        _, ext = os.path.splitext(video_path)
        if ext == '.mkv':
            format = None
        elif ext == '.avi':
            format = 'hevc'
        else:
            raise Exception("Unknown extension {}.".format(ext))
        return format

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        raw_image = self.video_pipe.stdout.read(self.h * self.w * 1)

        if len(raw_image) != self.h * self.w * 1:
            assert(len(raw_image) == 0)
            raise StopIteration()

        self.frames += 1

        image = np.fromstring(raw_image, dtype='uint8')
        image = image.reshape((self.h, self.w))
        self.video_pipe.stdout
        return image

    def kill(self):
        self.video_pipe.kill()


def create_list_dones_files():
    curr_date = iso8601.parse_date('2016-07-19')
    done_files = []
    while curr_date < iso8601.parse_date('2016-08-31'):
        done_files.append('{:%Y-%m-%d}'.format(curr_date))
        curr_date = curr_date + datetime.timedelta(days=1)
    return done_files


def get_first_frame(video_path):
    video_reader = VideoReader(video_path, None)
    img = next(video_reader)
    video_reader.kill()
    return img


def get_video_path(cam_id):
    root_path = '/mnt/storage/beesbook-data-clean/videos/high_res/hd/2016_oncray/'
    cam_path = '*/Cam_{cam_id}/Cam_{cam_id}*.mkv'.format(cam_id=cam_id)
    path = os.path.join(root_path, cam_path)
    return glob.glob(path)


def get_transformation_data(img_list, csv_out_path):
    img_pre = {'name': os.path.basename(img_list[0]),
               'data': get_first_frame(img_list[0])}
    for i, fn in enumerate(img_list[1:]):
        img_cur = {'name': os.path.basename(fn),
                   'data': get_first_frame(fn)}
        cc, mat = cust_findTransformECC(img_pre['data'], img_cur['data'])
        with open(csv_out_path, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            if mat is not None:
                mat = mat.tolist()
            row = [i, img_pre['name'], img_cur['name'], cc, mat]
            writer.writerow(row)
        img_pre = img_cur


def cust_findTransformECC(im1, im2, warp_mode=cv2.MOTION_TRANSLATION):

    # Define 2x3 or 3x3 matrices and initialze the matrix
    if warp_mode == cv2.MOTION_HOMOGRAPHY:
        warp_matrix = np.eye(3, 3, dtype=np.float32)
    else:
        warp_matrix = np.eye(2, 3, dtype=np.float32)

    # Specifiy the number of iterations
    number_of_iterations = 500

    # Specify the threshold of the increment
    # in the correlation coefficient between two iterations
    termination_eps = 1e-10

    # Define termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                number_of_iterations,  termination_eps)

    # Run the ECC algorithm.
    try:
        (cc, warp_matrix) = cv2.findTransformECC(im1, im2, warp_matrix, warp_mode, criteria)
    except cv2.error as e:
        cc = None
        warp_matrix = None
    return cc,  warp_matrix


path = '/mnt/storage/beesbook-data-clean/videos/high_res/hd/2016_oncray'
root_out = '/home/pst/2016_similarity_ecc'


video_paths = {}
for i in range(4):
    dict_key = 'Cam_{id}'.format(id=i)
    video_paths[dict_key] = get_video_path(i)
    video_paths[dict_key].sort()


# for cam in video_paths.keys():
for cam in ['Cam_0', 'Cam_1', 'Cam_2', 'Cam_3']:
    videos = video_paths[cam]
    out_path = os.path.join(root_out, cam + '.csv')
    get_transformation_data(videos, out_path)
