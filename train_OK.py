from ultralytics import YOLO
from base.logger import *

# 加载一个预训练的 YOLO8n 模型
model = YOLO("yolo8n.pt")

# # 在 COCO8 数据集上训练模型 100 个周期
# train_results = model.train(
#     data="coco8.yaml",  # 数据集配置文件路径
#     # data="default_detect.yaml",
#     epochs=1,  # 训练周期数
#     imgsz=640,  # 训练图像尺寸
#     device='cpu',  # 运行设备（例如 'cpu', 0, [0,1,2,3]）
# )

# device='cpu',  # 运行设备（例如 'cpu', 0, [0,1,2,3]）
# yolo detect train data=datasets/data.yaml model=yolo8n.pt epochs=5 batch=8 imgsz=640
train_results = model.train(
    data="datasets/data.yaml",  # 数据集配置文件路径
    model='yolov8n.pt',
    epochs=5,  # 训练周期数
    batch=8,
    imgsz=640,  # 训练图像尺寸
    device='cpu',  # 运行设备（例如 'cpu', 0, [0,1,2,3]）
)

# # 将模型导出为 ONNX 格式以进行部署
# path = model.export(format="onnx")  # 返回导出模型的路径
# logger.info(f'path:{path}')

logger.info(f'END')