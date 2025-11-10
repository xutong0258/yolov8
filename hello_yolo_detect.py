from ultralytics import YOLO
from base.logger import *


# Load a pretrained YOLO model (recommended for training)
model = YOLO("yolo8n.pt")

file = 'bus.jpg'
# results = model(file)  # 对图像进行预测
results = model.predict(file)  # 对图像进行预测
# logger.info(f'results:{results}')
results[0].show()