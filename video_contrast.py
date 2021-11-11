from tqdm import tqdm
import os
import sys
import cv2
import time
import numpy as np


def play_video(video1, video2, frame_size=(960, 540)):
    video_cap1 = cv2.VideoCapture(video1)
    video_cap2 = cv2.VideoCapture(video2)

    window_title = 'video contrast: ' + video1 + ', ' + video2
    cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_title, frame_size[0] * 2, frame_size[1])
    cv2.moveWindow(window_title, 0, 0)

    fps1 = video_cap1.get(cv2.CAP_PROP_FPS)
    fps2 = video_cap2.get(cv2.CAP_PROP_FPS)

    if fps1 > fps2:  # assume fps of video1 < fps of video2
        temp = video_cap1
        video_cap1 = video_cap2
        video_cap2 = temp

    millisecond_per_frame = int(1000.0 / fps2)

    frame_counts = int(video_cap1.get(cv2.CAP_PROP_FRAME_COUNT))

    progress_bar = tqdm(range(frame_counts - 1), ncols=100)
    start_time = time.time_ns() // 1_000_000

    for i in progress_bar:
        res, frame1 = video_cap1.read()
        if res != True:
            exit()
        res, frame2 = video_cap2.read()
        if res != True:
            exit()

        present_time1 = video_cap1.get(cv2.CAP_PROP_POS_MSEC)
        present_time2 = video_cap2.get(cv2.CAP_PROP_POS_MSEC)

        frame1 = cv2.resize(frame1, (frame_size[0], frame_size[1]))
        frame2 = cv2.resize(frame2, (frame_size[0], frame_size[1]))
        composite_frame = np.hstack((frame1, frame2))

        while (time.time_ns() // 1_000_000) < (start_time + present_time2):
            i = 1
        # print(present_time2)
        cv2.imshow(window_title, composite_frame)
        cv2.waitKey(1)

        res, frame2 = video_cap2.read()
        if res != True:
            exit()
        present_time2 = video_cap2.get(cv2.CAP_PROP_POS_MSEC)

        frame2 = cv2.resize(frame2, (frame_size[0], frame_size[1]))
        composite_frame = np.hstack((frame1, frame2))

        while (time.time_ns() // 1_000_000) < (start_time + present_time2):
            i = 1
        # print(present_time2)
        cv2.imshow(window_title, composite_frame)
        cv2.waitKey(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('please input 2 video path!')
        exit()

    if os.path.exists(sys.argv[1]) == False or os.path.exists(sys.argv[2]) == False:
        print('video not exist!')
        exit()

    video1 = sys.argv[1]
    video2 = sys.argv[2]

    play_video(video1, video2)
