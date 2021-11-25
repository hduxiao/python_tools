import sys
import os
import cv2
from tqdm import tqdm
import numpy as np


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


def visualize(image, faces, print_flag=False, fps=None):
    output = image.copy()

    if fps:
        cv2.putText(output, 'FPS: {:.2f}'.format(fps), (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

    for idx, face in enumerate(faces):
        if print_flag:
            print('Face {}, top-left coordinates: ({:.0f}, {:.0f}), box width: {:.0f}, box height {:.0f}, score: {:.2f}'.format(idx, face[0], face[1], face[2], face[3], face[-1]))

        coords = face[:-1].astype(np.int32)
        # Draw face bounding box
        cv2.rectangle(output, (coords[0], coords[1]), (coords[0]+coords[2], coords[1]+coords[3]), (0, 255, 0), 2)
        # # Draw landmarks
        # cv2.circle(output, (coords[4], coords[5]), 2, (255, 0, 0), 2)
        # cv2.circle(output, (coords[6], coords[7]), 2, (0, 0, 255), 2)
        # cv2.circle(output, (coords[8], coords[9]), 2, (0, 255, 0), 2)
        # cv2.circle(output, (coords[10], coords[11]), 2, (255, 0, 255), 2)
        # cv2.circle(output, (coords[12], coords[13]), 2, (0, 255, 255), 2)
        # Put score
        cv2.putText(output, '{:.4f}'.format(face[-1]), (coords[0], coords[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

    return output


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

    # Instantiate yunet
    yunet = cv2.FaceDetectorYN.create(
        model="./yunet.onnx",
        config='',
        input_size=(output_width, output_height),
        score_threshold=0.9,
        nms_threshold=0.3,
        top_k=5000,
        backend_id=cv2.dnn.DNN_BACKEND_CUDA,
        target_id=cv2.dnn.DNN_TARGET_CUDA
    )

    progress_bar = tqdm(range(images_count), ncols=100)
    for i in progress_bar:
        sample = cv2.imread(images[i])
        height, width, channels = sample.shape

        facedetect_results = []
        yunet.setInputSize((width, height))
        _, facedetect_results = yunet.detect(sample)

        if not facedetect_results is None:
            print(facedetect_results)
            output = visualize(sample, facedetect_results)
        else:
            output = sample

        sample = cv2.resize(output, (output_width, output_height), interpolation = cv2.INTER_CUBIC)
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
