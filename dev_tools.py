import os


def find_target_files(dir, file_extension):
    files_list = []
    if os.path.isdir(dir):
        all_files = os.listdir(dir)
        for file in all_files:
            file_path = os.path.join(dir, file)
            if os.path.isfile(file_path) and file_path.lower().endswith(file_extension):
                files_list.append(file_path)
    print('find target files:', files_list)
    return files_list
