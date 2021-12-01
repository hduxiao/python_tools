from dev_tools import *
import sys
from tqdm import tqdm
import cv2


def images_to_video(images_path, fps=1, frame_size=(1280, 720), out_video=""):
    images = find_target_files(images_path, ('.bmp', '.dib', '.png', '.jpg', '.jpeg',
                                             '.pbm', '.pgm', '.ppm', '.tif', '.tiff'))
    images_count = len(images)

    if images_count == 0:
        print("there are no images under this path!")
        exit()

    if len(out_video) == 0:
        out_video = images_path + '.mp4'

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    output_writer = cv2.VideoWriter(out_video, fourcc, fps, frame_size)
    print('output video:', out_video)

    progress_bar = tqdm(range(images_count), ncols=100)
    for i in progress_bar:
        sample = cv2.imread(images[i])
        sample = cv2.resize(sample, frame_size, interpolation=cv2.INTER_CUBIC)
        output_writer.write(sample)


if __name__ == '__main__':
    argv = sys.argv
    argc = len(argv)

    if argc != 2:
        print("please input the images path!")
        exit()

    images_path = argv[1]
    images_to_video(images_path)
