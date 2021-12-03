from dev_tools import *
import sys
import os
from tqdm import tqdm
import cv2
import numpy as np


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
        cv2.circle(output, (coords[4], coords[5]), 2, (255, 0, 0), 2)
        cv2.circle(output, (coords[6], coords[7]), 2, (0, 0, 255), 2)
        cv2.circle(output, (coords[8], coords[9]), 2, (0, 255, 0), 2)
        cv2.circle(output, (coords[10], coords[11]), 2, (255, 0, 255), 2)
        cv2.circle(output, (coords[12], coords[13]), 2, (0, 255, 255), 2)
        # Put score
        cv2.putText(output, '{:.4f}'.format(face[-1]), (coords[0], coords[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

    return output


def images_facedetect(images_path, output_path):
    images = find_target_files(images_path, ('.bmp', '.dib', '.png', '.jpg', '.jpeg',
                                             '.pbm', '.pgm', '.ppm', '.tif', '.tiff'))

    # Instantiate yunet
    yunet = cv2.FaceDetectorYN.create(
        model="./yunet.onnx",
        config='',
        input_size=(1920, 1080),
        score_threshold=0.9,
        nms_threshold=0.3,
        top_k=5000,
        backend_id=cv2.dnn.DNN_BACKEND_CUDA,
        target_id=cv2.dnn.DNN_TARGET_CUDA
    )

    images_count = len(images)
    progress_bar = tqdm(range(images_count), ncols=100)
    for i in progress_bar:
        sample = cv2.imread(images[i][1])

        height = sample.shape[0]
        width = sample.shape[1]
        facedetect_results = []
        yunet.setInputSize((width, height))
        _, facedetect_results = yunet.detect(sample)

        if not facedetect_results is None:
            print(facedetect_results)
            output = visualize(sample, facedetect_results)
        else:
            output = sample

        output_image_path = os.path.join(output_path, images[i][0])
        cv2.imwrite(output_image_path, output)


if __name__ == '__main__':
    argc = len(sys.argv)

    if argc != 3:
        print("please input images path and output path!")
        exit()

    images_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(images_path) or not os.path.exists(output_path):
        print("path not exist!")
        exit()

    images_facedetect(images_path, output_path)
