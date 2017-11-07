import argparse
import cv2
import os
import time

import video_reader


def process_videos(video_path, ts_file, out_path, ts):
    vr = video_reader.VideoReader(video_path)
    # cap = cv2.VideoCapture(args.video_path)

    with open(ts_file, 'rU') as f:
        content = [x.strip('\n') for x in f.readlines()]

    for i, stamp in enumerate(content):
        frame = next(vr)
        if stamp == ts:
            cv2.imwrite(os.path.join(out_path, stamp+'.jpg'), frame)
            vr.kill()
            break


def main():
    parser = argparse.ArgumentParser(
        prog='BeesBook Video cutter',
        description='Get frames from a BeesBook Video with timesamps as names.'
    )

    parser.add_argument('video_path', help='Path of the video.', type=str)
    parser.add_argument('ts_file', help='Path of the file which holds the timestamps of the frames.', type=str)
    parser.add_argument('out_path', help='Path for the output images.', type=str)
    parser.add_argument('ts', help='Frame to get.', type=str)
    args = parser.parse_args()
    process_videos(args.video_path, args.ts_file, args.out_path, args.ts)

if __name__ == '__main__':
    main()
