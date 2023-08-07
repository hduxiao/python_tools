import os
from tqdm import tqdm
import cv2
import argparse
import numpy as np
import math

def find_target_files(dir, file_extension):
    files_list = []
    if os.path.isdir(dir):
        all_files = os.listdir(dir)
        for file in all_files:
            file_path = os.path.join(dir, file)
            if os.path.isfile(file_path) and file_path.lower().endswith(file_extension):
                    files_list.append((file, file_path))
    # print('find target files:', files_list)
    return files_list


def merge_videos(args):
    videos1 = find_target_files(args.input1, '.mp4')
    videos2 = find_target_files(args.input2, '.mp4')
    videos3 = find_target_files(args.input3, '.mp4')
    videos4 = find_target_files(args.input4, '.mp4')
    if len(videos2) != len(videos1) or len(videos3) != len(videos1) or len(videos4) != len(videos1):
        print('error')
        return

    output_dir = args.output
    if output_dir is None:
        output_dir = os.path.dirname(args.input1) + '/Comparison Video'

    labels = []
    labels.append(os.path.basename(args.input1))
    labels.append(os.path.basename(args.input2))
    labels.append(os.path.basename(args.input3))
    labels.append(os.path.basename(args.input4))

    input_lists = []
    for i in range(len(videos1)):
        input_list = [videos1[i], videos2[i], videos3[i], videos4[i]]
        input_lists.append(input_list)

    for input_list in input_lists:
        vcs = []
        width0 = 0
        height0 = 0
        total_frame0 = 0
        fps0 = 0
        for input in input_list:
            vc = cv2.VideoCapture()
            vc.open(input[1])
            if not vc.isOpened():
                print("Open file {} failed".format(input[1]))
                exit()
            vcs.append(vc)
            total_frame = vc.get(cv2.CAP_PROP_FRAME_COUNT)
            in_width = vc.get(cv2.CAP_PROP_FRAME_WIDTH)
            in_height = vc.get(cv2.CAP_PROP_FRAME_HEIGHT)
            fps = vc.get(cv2.CAP_PROP_FPS)
            if width0 == 0:
                width0 = in_width
                height0 = in_height
                total_frame0 = total_frame
                fps0 = fps
            else:
                if in_width != width0 or in_height != height0 or math.fabs(fps0 - fps) > 0.1:
                    print("inconsistent resolution ({}, {}) with ({}, {}), or fps {} with {}".format(
                        width0, height0, in_width, in_height, fps0, fps))
                    exit()
                if total_frame < total_frame0:
                    total_frame0 = total_frame
        out_width = width0 * 2
        out_height = height0 * 2
        frame_size = (int(out_width), int(out_height))
        out_video = output_dir + '/' + input_list[0][0]
        vw = cv2.VideoWriter(out_video, cv2.VideoWriter_fourcc(*'mp4v'), fps=fps0, frameSize=frame_size)
        print('output video:', out_video)
        if not vw.isOpened():
            print("Open output file {} failed".format(out_video))

        for i in tqdm(range(int(total_frame0))):
            imgs = []
            for i in range(4):
                ret, img = vcs[i].read()
                if not ret:
                    break
                fontScale = out_width / 2560
                org = (np.uint8(50 * fontScale), np.uint8(50 * fontScale))
                thickness = np.uint8(2 * fontScale)
                cv2.putText(img, labels[i], org, cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 0, 255), thickness)
                imgs.append(img)
            if len(imgs) != 4:
                break
            img_left = np.concatenate([imgs[0], imgs[2]], axis=0)
            img_right = np.concatenate([imgs[1], imgs[3]], axis=0)
            img_out = np.concatenate([img_left, img_right], axis=1)
            vw.write(img_out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input1', type=str, help='upper left video file folder')
    parser.add_argument('input2', type=str, help='upper right video file folder')
    parser.add_argument('input3', type=str, help='bottom left video file folder')
    parser.add_argument('input4', type=str, help='bottom right video file folder')
    parser.add_argument('-o', '--output', type=str, help='Output path')
    args = parser.parse_args()

    merge_videos(args)


if __name__ == '__main__':
    main()
