# coding=utf-8

import yaml
import json
import os
import platform

def read_file_by_line(file_name: str) -> list:
    """
    读取文本用例数据
    :param file_name: 文件路径
    :return: list
    """
    with open (file_name, "r") as file:
        for line in file:
            # my_log.info (line.strip ())
            pass
    return

def get_case_data_list(file_name: str) -> list:
    """
    读取文本用例数据
    :param file_name: 文件路径
    :return: list
    """
    with open(file_name, mode="r", encoding="utf-8") as f:
        data_list = f.readlines()
    data_list = [line.strip() for line in data_list]
    return data_list

def read_yaml_dict(file_name: str) -> dict:
    """
    读取文本用例数据
    :param file_name: 文件路径
    :return: list
    """
    data_dic = {}
    with open(file_name, 'r', encoding='utf-8') as wf:
        record_dic = yaml.safe_load(wf)
    return record_dic

def read_file_dict(file_name: str) -> dict:
    record_dic = {}
    if '.yaml' in file_name:
        with open(file_name, 'r', encoding='utf-8') as wf:
            record_dic = yaml.safe_load(wf)
    elif '.json' in file_name:
        with open (file_name, 'r') as wf:
            record_dic = json.load (wf)
    else:
        # my_log.info(f'file not support:{read_file_dict}')
        pass
    return record_dic

def dump_file(file_name, data) -> int:
    """
    读取文本用例数据
    :param file_name: 文件路径
    :return: list
    """
    # file_name = os.path.join(file_path, file_name)

    yaml_support = True
    if yaml_support:
        with open(file_name, 'w', encoding='utf-8') as wf:
            yaml.safe_dump(data, wf, default_flow_style=False, allow_unicode=True)
    else:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    return 0

def dump_json(file_name: str, data: dict) -> int:
    """
    读取文本用例数据
    :param file_name: 文件路径
    :return: list
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return 0

def read_json_dict(file_name: str) -> dict:
    """
    读取文本用例数据
    :param file_name: 文件路径
    :return: list
    """
    data_dic = {}
    with open(file_name, 'r') as wf:
        data_dic = json.load(wf)
    return data_dic

def read_file_str(file_name):
    """
    读取文本用例数据
    :param file_name: 文件路径
    :return: list
    """
    # 打开文件，返回一个文件对象
    with open(file_name, 'r', encoding='gbk') as file:
        # 读取文件的全部内容
        content = file.read ()
        # my_log.info(content)
    return content

def wrtie_file(file_name, content) -> None:
    # 打开文件，如果文件不存在，会创建文件；'a' 表示追加模式，如果文件已存在，则会在文件末尾追加内容
    with open (file_name, 'w') as file:
        # 追加文本数据
        file.write(content)
    return

def add_string_to_first_line(file_path, new_string):
    try:
        # 以只读模式打开文件并读取所有内容
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 在内容开头插入新的字符串，并添加换行符
        lines.insert(0, new_string + '\n')

        # 以写入模式打开文件并将更新后的内容写回
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

        # print(f"成功在文件 {file_path} 的第一行添加字符串。")
    except FileNotFoundError:
        print(f"未找到文件: {file_path}")
    except Exception as e:
        print(f"发生错误: {e}")
    return

def change_file_dict():
    file_name = r'D:\0_rope_skip_VIP\跳绳_last_model_count_VIP.yaml'
    data_dic = read_file_dict (file_name)
    target_dict = {}
    for file, file_dict in data_dic.items():
        new_file_dict = {}
        for key, value in file_dict.items():
            cell_dict = {}
            cell_dict.update({'fakeJumpTimes': 0})
            cell_dict.update ({'number': value})
            new_file_dict.update({f'{key}': cell_dict})
        target_dict.update({f'{file}': new_file_dict})

    # file = os.path.join (LOG_DIR, '跳绳_last_model_count_VIP.yaml')
    # dump_file (file, target_dict)
    return

def change_file_format():
    file_name = r'D:\configure_model_v2.8.0.json'
    data_dic = read_json_dict (file_name)

    file_name = r'D:\configure_model_v2.8.0_new.json'
    dump_json (file_name, data_dic)
    return

if __name__ == '__main__':
    # change_file_format()
    # change_file_dict()
    # covert_rope_cfg()
    # rope_analysis()
    current_enable = False
    if current_enable:
        data_dict = {}
        file = r'D:/hello.yaml'
        dump_file(file, data_dict)
    else:
        pass