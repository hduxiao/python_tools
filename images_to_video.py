import os
import sys
from tqdm import tqdm
import cv2
import argparse

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


def images_to_video(args):
    images = find_target_files(args.input, ('.bmp', '.dib', '.png', '.jpg', '.jpeg',
                                             '.pbm', '.pgm', '.ppm', '.tif', '.tiff'))
    images_count = len(images)

    if images_count == 0:
        print("there are no images under this path!")
        exit()

    out_video = args.output
    if out_video is None:
        out_video = args.input + '.mp4'

    framesize = args.framesize
    if framesize is None:
        framesize = [320, 640]

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    output_writer = cv2.VideoWriter(out_video, fourcc, args.framerate, framesize)
    print('output video:', out_video)

    progress_bar = tqdm(range(images_count), ncols=100)
    for i in progress_bar:
        sample = cv2.imread(images[i][1])
        sample = cv2.resize(sample, framesize, interpolation=cv2.INTER_CUBIC)
        output_writer.write(sample)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='Images folder')
    parser.add_argument('-f', '--framerate', type=float, default='12.5', help='Video framerate')
    parser.add_argument('-s', '--framesize', type=int, nargs=2, help='Video framesize(width, height)')
    parser.add_argument('-o', '--output', type=str, help='Output path')
    args = parser.parse_args()

    images_to_video(args)


if __name__ == '__main__':
    main()
