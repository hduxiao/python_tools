"""
A python script transfer video into images.
It supports any OpenCV file format.

Author: Thomas
License: Apache
Version: 0.0.1
Email: thomas@graphopti.com
Data: 2022-10-31
"""

import argparse
import math
import os
import sys

import cv2

# --help / -H argument
# --input / -i
# --output or -o
parser = argparse.ArgumentParser(
    description="",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-o", "--output_type", type=str, default="jpeg", help="output file type"
)
parser.add_argument("-f", "--fps", type=int, default=-1, help="Store frames per second")
parser.add_argument("src", help="Source location, should be a video file type")
parser.add_argument("dest", help="Destination folder location")
args = parser.parse_args()
config = vars(args)
print("Startring video_to_images.py with configuration:", config)


file_source = args.src
file_destination = args.dest

# checking video
video_cap = cv2.VideoCapture(file_source)
# check file exits
if video_cap.isOpened() == False:
    print("Can not open file:" + file_source)
    exit()
video_fps = video_cap.get(cv2.CAP_PROP_FPS)
if args.fps == -1:
    fps = video_fps
else:
    if args.fps > video_fps:
        fps = video_fps
    else:
        if args.fps >= 1:
            fps = args.fps
        else:
            fps = video_fps

if not os.path.exists(args.dest):
    os.makedirs(args.dest)
print("Video origin Frame rate: ", int(video_fps), " FPS. Current set to ", int(fps))
ticker = 0
ticker_step = math.floor(video_fps / fps)
image_count = 1
while True:
    ret, frame = video_cap.read()
    ticker += 1
    if not ret:
        break
    if ticker >= ticker_step:
        ticker = 0
        save_str = str(image_count) + "." + args.output_type
        image_count += 1
        os.chdir(args.dest)
        cv2.imwrite(save_str, frame)
        print("Writing ", save_str, "...")
video_cap.release()
