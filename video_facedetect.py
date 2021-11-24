import sys
import os
import cv2
from tqdm import tqdm
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
        # cv2.circle(output, (coords[4], coords[5]), 2, (255, 0, 0), 2)
        # cv2.circle(output, (coords[6], coords[7]), 2, (0, 0, 255), 2)
        # cv2.circle(output, (coords[8], coords[9]), 2, (0, 255, 0), 2)
        # cv2.circle(output, (coords[10], coords[11]), 2, (255, 0, 255), 2)
        # cv2.circle(output, (coords[12], coords[13]), 2, (0, 255, 255), 2)
        # Put score
        cv2.putText(output, '{:.4f}'.format(face[-1]), (coords[0], coords[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

    return output


def main():
    argv = sys.argv
    argc = len(argv)

    if argc != 2:
        print("please input a video!")
        exit()

    input_video_path = argv[1]
    if os.path.exists(input_video_path) == False:
        print("input video path not exist!")
        exit()

    input_video_cap = cv2.VideoCapture(input_video_path)
    input_video_fps = input_video_cap.get(cv2.CAP_PROP_FPS)
    input_video_height = int(input_video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    input_video_width = int(input_video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    input_video_frame_count = int(input_video_cap.get(cv2.CAP_PROP_FRAME_COUNT))

    output_path = input_video_path + "facedetect.avi"
    output_fps = input_video_fps
    # output_height = input_video_height
    # output_width = input_video_width
    # output_height = 240
    # output_width = 320
    output_height = 480
    output_width = 640
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

    progress_bar = tqdm(range(input_video_frame_count), ncols=100)
    for i in progress_bar:
        hr, sample = input_video_cap.read()
        if hr == False:
            break
        
        sample = cv2.resize(sample, (output_width, output_height), interpolation = cv2.INTER_CUBIC)

        facedetect_results = []
        _, facedetect_results = yunet.detect(sample)

        if not facedetect_results is None:
            print(facedetect_results)
            vis_results = visualize(sample, facedetect_results)
            output_writer.write(vis_results)
        else:
            output_writer.write(sample)
        

if __name__ == "__main__":
    main()
