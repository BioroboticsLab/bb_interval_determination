import cv2
import numpy as np
import os
import subprocess as sp

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


def get_first_frame(video_path):
    video_reader = VideoReader(video_path, None)
    first_frame = next(video_reader)
    video_reader.kill()
    return first_frame


def get_last_frame(video_path):
    video_reader = VideoReader(video_path, None)
    for last_frame in video_reader:
        pass
    video_reader.kill()
    return last_frame
