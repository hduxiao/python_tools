from tqdm import tqdm
import os
import sys
import cv2
import time
import numpy as np


def slow_video(video_path, output_path, slow_times):
    video_cap = cv2.VideoCapture(video_path)

    video_fps = video_cap.get(cv2.CAP_PROP_FPS)
    new_fps = video_fps / slow_times

    width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frame_count = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))

    video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(
        'M', 'J', 'P', 'G'), new_fps, (width, height))

    progress_bar = tqdm(range(frame_count), ncols=100)
    for i in progress_bar:
        res, sample = video_cap.read()
        if res != True:
            break
        video_writer.write(sample)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('please input 2 video path and 1 slowdown time!')
        exit()

    if os.path.exists(sys.argv[1]) == False:
        print('video not exist!')
        exit()

    video_input = sys.argv[1]
    video_output = sys.argv[2]
    slow_times = float(sys.argv[3])

    if video_input == video_output:
        exit()

    slow_video(video_input, video_output, slow_times)
