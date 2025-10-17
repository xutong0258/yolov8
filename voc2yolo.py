import os
import xml.etree.ElementTree as ET
import glob

# 设置路径
voc_images_path = "VOC_dataset/JPEGImages/"  # 图片所在路径
voc_images_path = r"D:\祥源城"  # 图片所在路径

voc_annotations_path = "VOC_dataset/Annotations/"  # XML标注所在路径
voc_annotations_path = r"D:\祥源城"  # XML标注所在路径

yolo_labels_path = "YOLO_dataset/labels/"  # 转换后的YOLO标注存放路径
yolo_labels_path = r"D:\祥源城\yolo"  # 转换后的YOLO标注存放路径

yolo_images_path = "YOLO_dataset/images/"  # 图片复制目标路径
yolo_images_path = r"D:\祥源城\yolo_img"  # 图片复制目标路径

sets = ["train", "val", "test"]  # 数据集划分

# 类别列表，根据你的数据集修改
classes = ["class1", "class2", "class3"]  # 替换为你的实际类别

# 创建输出目录
os.makedirs(yolo_labels_path, exist_ok=True)
os.makedirs(yolo_images_path, exist_ok=True)
for set_name in sets:
    os.makedirs(os.path.join(yolo_labels_path, set_name), exist_ok=True)
    os.makedirs(os.path.join(yolo_images_path, set_name), exist_ok=True)


def convert(size, box):
    """将VOC的xmin, ymin, xmax, ymax转换为YOLO的归一化坐标"""
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id, set_name):
    """转换单个XML文件为YOLO格式的txt文件"""
    in_file = open(f"{voc_annotations_path}/{image_id}.xml", encoding='utf-8')
    out_file = open(f"{yolo_labels_path}/{set_name}/{image_id}.txt", 'w', encoding='utf-8')

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(f"{cls_id} " + " ".join([f"{a:.6f}" for a in bb]) + '\n')

    in_file.close()
    out_file.close()


# 处理每个数据集划分
for set_name in sets:
    image_ids = open(f"VOC_dataset/ImageSets/Main/{set_name}.txt").read().strip().split()

    # 转换标注并复制图片
    for image_id in image_ids:
        # 转换标注
        convert_annotation(image_id, set_name)

        # 复制图片到YOLO数据集目录
        img_src = f"{voc_images_path}/{image_id}.jpg"
        img_dst = f"{yolo_images_path}/{set_name}/{image_id}.jpg"

        # 如果图片是png格式，这里需要修改
        if not os.path.exists(img_src):
            img_src = f"{voc_images_path}/{image_id}.png"
            img_dst = f"{yolo_images_path}/{set_name}/{image_id}.png"

        if os.path.exists(img_src):
            # 使用硬链接复制，节省空间
            if not os.path.exists(img_dst):
                os.link(img_src, img_dst)
        else:
            print(f"警告: 图片文件 {img_src} 不存在")

print("转换完成！")