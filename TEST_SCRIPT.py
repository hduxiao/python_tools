import os
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='Input folder')
    parser.add_argument('output', type=str, help='Output folder')
    args = parser.parse_args()
    videos = find_target_files(args.input, '.mp4')
    for video in videos:
        input_path = video[1]
        output_path = args.output + '/' + video[0]
        cmd = r"python C:\\Users\\NERO\Desktop\\mmagic-main\demo\\mmagic_inference_demo.py --model-name basicvsr_pp --video " + input_path + " --result-out-dir " + output_path + " --extra-parameters max_seq_len=10"
        print(cmd)
        os.system(cmd)


if __name__ == '__main__':
    main()
