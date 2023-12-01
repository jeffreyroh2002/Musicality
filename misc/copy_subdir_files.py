import os
import shutil
import time

def read_all_file(path):
    output = os.listdir(path)
    file_list = []

    for i in output:
        if os.path.isdir(path+"/"+i):
            file_list.extend(read_all_file(path+"/"+i))
        elif os.path.isfile(path+"/"+i):
            file_list.append(path+"/"+i)

    return file_list

def copy_all_file(file_list, new_path):
    for src_path in file_list:
        file = src_path.split("/")[-1]
        shutil.copyfile(src_path, new_path+"/"+file)
        print("file {} done".format(file)) # print file name
        
        
start_time = time.time() # 작업 시작 시간 

src_path = "../EpidemicSoundRaw/audio_full_mix/" # input dir
new_path = "../EpidemicSoundRaw/full_mix/" # output dir

os.makedirs(new_path, exist_ok=True)

file_list = read_all_file(src_path)
copy_all_file(file_list, new_path)

