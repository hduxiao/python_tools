import cv2
import numpy as np
import insightface
from tqdm import tqdm
import os
import sys
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image


def find_subdir(path):
    dirlist = []
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files:
            tmp = os.path.join(path, file)
            if os.path.isdir(tmp):
                dirlist.append(tmp)
    return dirlist


def find_images(path):
    imagelist = []
    for parent, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                imagelist.append(os.path.join(parent, filename))
    return imagelist


def images_to_video(images_path):
    images = find_images(images_path)
    images_count = len(images)
    if images_count == 0:
        print("there are no images under this path!")
        exit()

    output_path = os.path.join(os.path.dirname(images_path), os.path.basename(images_path) + '.avi')
    output_fps = 1
    output_height = 768
    output_width = 1024
    output_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MJPG'), output_fps, (output_width, output_height))

    app = FaceAnalysis(allowed_modules=['detection'])
    app.prepare(ctx_id=0, det_size=(640, 640))
    

    progress_bar = tqdm(range(images_count), ncols=100)
    for i in progress_bar:
        img = cv2.imread(images[i])
        faces = app.get(img)
        rimg = app.draw_on(img, faces)

        sample = cv2.resize(rimg, (output_width, output_height), interpolation = cv2.INTER_CUBIC)
        cv2.putText(sample, images[i], (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
        output_writer.write(sample)


def main():
    argv = sys.argv
    argc = len(argv)

    if argc != 2:
        print("please input the images path!")
        exit()

    images_path = argv[1]

    dirlist = find_subdir(images_path)
    for dir in dirlist:
        images_to_video(dir)
        

if __name__ == "__main__":
    main()
