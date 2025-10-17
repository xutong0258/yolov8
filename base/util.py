# coding=utf-8

import json
import os
import shutil
import sys
import logging
import time
import datetime
import re
from base import fileOP
import cv2

# file = os.path.abspath(__file__)
path_dir = os.path.dirname(__file__)

LOG_DIR = os.path.join(path_dir, f"../../auto_test_log")
# print(f'LOG_DIR:{LOG_DIR}')

if not os.path.exists(LOG_DIR):
    # print(f'os.mkdir:{LOG_DIR}')
    os.mkdir(LOG_DIR)


time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
filename = f'test_{time_stamp}.log'

# 获取日志文件的绝对路径
log_file = os.path.join(LOG_DIR, filename)

formatter2 = logging.Formatter(
    '[%(asctime)s]'
    '%(filename)s'
    '[Line:%(lineno)d]: '
    '%(message)s'
)

CH = logging.StreamHandler()
CH.setLevel(logging.DEBUG)
CH.setFormatter(formatter2)

global current_enable
current_enable = False

if current_enable:
    LOG = logging.getLogger(__file__)
    LOG.setLevel (logging.DEBUG)
    LOG.addHandler (CH)

_format =('[%(asctime)s][%(filename)s][%(funcName)s][%(lineno)s]'
' %(levelname)s: %(message)s')

# for differnt module, different log

def init_logger(loggername, file=None):
    logger = logging.getLogger(loggername)
    logger.setLevel(level=logging.DEBUG)
    if not logger.handlers and file:
        file_handler = logging.FileHandler(file, encoding="utf8")
        file_format = logging.Formatter(_format)
        file_handler.setFormatter(file_format)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.addHandler(CH)
    return logger

print(f'log_file:{log_file}')
logger = init_logger('HELLO', log_file)
logger.info('hello')

# os.system
def cmd_excute(cmd, logger=None, outfile=None, errfile=None):
    if outfile is None and errfile is None:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        # result = stdout.decode('utf-8').strip('\r\n')
        result = stdout
        errors = stderr
        return_code = process.returncode
        msg = result if not stderr else errors
        if logger:
            logger.info(cmd)
            logger.debug(return_code)
            if return_code != 0:
                logger.error(errors)

        return result, errors, return_code
    else:
        f_out = open(outfile, 'w')
        f_err = open(errfile, 'w')
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=f_out,
            stderr=f_err)
        output, errors = process.communicate()
        return_code = process.returncode
        if logger:
            logger.info(cmd)
            logger.debug(return_code)
        if return_code != 0:
            logger.error(errors)

        return return_code

def replace_file():
    wait_str = ''
    target_str = ''
    current_dir = r'D:\00_stone_project-237\0_17_stress_cases'
    target_dirs = os.listdir(current_dir)
    final_list = []
    for item in target_dirs:
        path = os.path.join(current_dir, item)
        command = f"cd {path} && sed -i 's/{wait_str}/{target_str}/g' *.yaml"
        cmd_excute(command)

    return

def clean_file():
    C1_Time = datetime.datetime.now ()
    logger.info(f'curreent:{C1_Time}')
    time_stamp = datetime.datetime.now ().strftime ("%Y-%m-%d %H:%M:%S")
    logger.info(f'time_stamp:{time_stamp}')

    # current_dir = os.getcwd()
    for root, dirs, files in os.walk(path_dir):
        for file in files:
            if '.mp4' not in file:
                continue
            file = os.path.join(root, file)

            c2_Time = os.path.getmtime(file)
            c2_Time = datetime.datetime.fromtimestamp(c2_Time)
            delta = C1_Time.__sub__ (c2_Time)
            logger.info(f'delta.days:{delta.days}')
            if delta.days > 5:
                logger.info (f"remove file:{file} delta.days:{delta.days}")
                cmd = f'sudo rm -rf {file}'
                cmd_excute(file)
    return

def copy_file_shutil():
    C1_Time = datetime.datetime.now ()
    logger.info(f'curreent:{C1_Time}')
    time_stamp = datetime.datetime.now ().strftime ("%Y-%m-%d %H:%M:%S")
    logger.info(f'time_stamp:{time_stamp}')

    # current_dir = os.getcwd()
    for root, dirs, files in os.walk(path_dir):
        for file in files:
            if '203' in file:
                dest_file = os.path.join(path_dir, '../total', file)
                source_file = os.path.join(root, file)
                shutil.copyfile(source_file, dest_file)

    return

def install_package_by_file():
    file_name = 'requirements.txt'
    with open (file_name, "r") as file:
        for line in file:
            line = line.strip()
            cmd = f'sudo pip install {line} -i https://mirrors.aliyun.com/pypi/simple/'
            result, errors, return_code = cmd_excute (cmd)
            logger.info (f'result:{result}, errors:{errors}, return_code:{return_code}')


def convert_file_to_265(video_path_dir_list, scale=None):
    # scale=3840:2160
    if scale:
        pass
    else:
        scale = 'scale=1920:1080'

    if not video_path_dir_list:
        video_path_dir_list = list()
        video_path_dir_list.append(r'D:\99_TEST_VIDEO\00_stand_jump_model_0\hand_hold_jump\驻马店职业技术学院_new')

    # video_path_dir = os.getcwd()
    for item in video_path_dir_list:
        files = os.listdir(item)
        str_cmd = f'cd {item}'

        result, errors, return_code = cmd_excute(str_cmd)
        logger.info(f'result:{result}, errors:{errors}, return_code:{return_code}')

        for file_name in files:
            logger.info (f'file_name:{file_name}')
            if '.mp4' not in file_name:
                continue
            # out_file = file_name.replace('.mp4', '_output.mp4')
            out_file = os.path.join(item, 'output', file_name)
            file = os.path.join(item, file_name)
            str_cmd = f'ffmpeg -i {file} -vf "{scale}" -c:v libx265  -c:a copy {out_file}'
            # cmd = f'ffmpeg -i {file} -vf "scale=1920:1080" -q:v 20 -b:v 2M -c:v libx265 -c:a copy {out_file}'
            result, errors, return_code = cmd_excute(str_cmd)
            logger.info(f'result:{result}, errors:{errors}, return_code:{return_code}')
    logger.info ('end')
    return



def file_walk():
    # 要遍历的文件夹路径
    folder_path = "your_folder_path"
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            if '.avi' in file_path:
                logger.info (f'rm :{file_path}')
                str_cmd = f'rm -rf {file_path}'
                result, errors, return_code = cmd_excute (str_cmd)
                logger.info (f'result:{result}, errors:{errors}, return_code:{return_code}')


    return

def count_file():
    work_dir = r'D:\0_rope_skip_VIP\patch'
    work_dir_list = os.listdir (work_dir)
    total_file = 0
    for item in work_dir_list:
        full_path = os.path.join(work_dir, item)
        logger.info (f'full_path:{full_path}')
        if os.path.isfile(full_path):
            continue

        sub_list = os.listdir (full_path)
        file_count = len (sub_list)

        logger.info (f'file_count:{file_count}')

        total_file += file_count

    logger.info (f'total_file:{total_file}')
    return


def copy_file_by_list():
    file_list = ['2024_12_15_15_50_38_192.168.2.206_1_1_A_face_13_24级大数据会计-管理会计-一班_1080p.mp4']
    file_list.append('2024_12_15_19_58_4_192.168.2.206_1_1_A_face_13_24级计算机应用技术java1班_1080p.mp4')
    file_list.append ('2024_12_16_10_39_1_192.168.2.206_1_1_A_face_15_2022级五年制计算机应用技术01班_1080p.mp4')
    file_list.append ('2024_12_16_11_24_1_192.168.2.206_1_1_A_face_15_2022级五年制计算机应用技术01班_1080p.mp4')
    file_list.append ('2024_12_16_14_34_38_192.168.2.206_1_1_A_face_16_21五年制会计电商_1080p.mp4')
    file_list.append ('2024_12_20_14_44_54_192.168.2.206_1_1_A_face_13_24级数字媒体技术1班_1080p.mp4')
    file_list.append ('2024_12_20_17_33_30_192.168.2.206_1_1_A_face_13_24级计算机应用技术java1班_1080p.mp4')
    file_list.append ('2024_12_22_15_41_7_192.168.2.206_1_1_A_face_14_2023级建筑智能化工程技术-智能楼宇工程-01班_1080p.mp4')
    # file_list.append ('')
    # file_list.append ('')
    # file_list.append ('')
    # file_list.append ('')
    work_dir = r'D:\99_TEST_VIDEO\00_stand_jump_model_0\hand_hold_jump\驻马店职业技术学院_new'
    for item in file_list:
        source_file = os.path.join(work_dir, item)
        target_file = os.path.join (work_dir, 'output', item)
        cmd = f'cp {source_file} {target_file}'
        logger.info (f'cmd:{cmd}')
        result, errors, return_code = cmd_excute(cmd)
        logger.info (f'result:{result}, errors:{errors}, return_code:{return_code}')

    return

import subprocess

def get_video_duration_ffprobe(video_path):
    command = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    result = 0
    try:
        result = subprocess.check_output(command).decode('utf-8').strip()
    except Exception as ex:
        print(f'Exception:{ex}')
        result = 0
    finally:
        pass
    return float(result)

def split_list(lst, num):
    length = len(lst)
    part_length = length // num  # 计算每一部分的长度
    remainder = length % num  # 计算余数
    parts = []
    start = 0
    for i in range(num):
        if i < remainder:  # 对于余数部分，将长度加 1
            end = start + part_length + 1
        else:
            end = start + part_length
        parts.append(lst[start:end])  # 截取列表的一部分添加到结果中
        start = end
    return parts

def get_video_resolution(video_path):
    # video_path = r'D:\test\concat.mp4'
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("无法打开视频文件，请检查文件路径是否正确。")
    # 获取视频的宽度
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # 获取视频的高度
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # 释放视频文件
    cap.release()
    logger.info (f'width:{width}, height:{height}')
    return width, height

def change_file_name():
    dir = r'D:\0_慧务农\发票\bak\11'
    # /home/yskj/data/sport-ci/conf
    # dir = r'/home/yskj/data/sport-ci/conf'
    tmp_list = os.listdir (dir)
    for item in tmp_list:
        full_path = os.path.join(dir, item)
        new_path = full_path.replace('.pdf', '_33.pdf')
        command = f'mv {full_path} {new_path}'
        # cmd_excute(command, logger)
        os.rename(full_path, new_path)

    return

if __name__ == '__main__':
    change_file_name()
    # get_video_resolution(video_path=None)
    # convert_file_to_265(video_path_dir_list)
    # sort_file()
    # replace_file()
    # copy_file_shutil()
    # install_package_by_file()
    # file_walk()
    # count_file()
    # copy_file_by_list()
    pass
