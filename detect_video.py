# 安装必要的库（如果尚未安装）
# !pip install ultralytics opencv-python

from ultralytics import YOLO
import cv2
import os


def detect_video(input_video_path, output_video_path=None, conf_threshold=0.25):
    """
    使用YOLOv8n模型对视频进行目标检测

    参数:
        input_video_path: 输入视频的路径
        output_video_path: 输出视频的保存路径，若为None则不保存
        conf_threshold: 置信度阈值，默认为0.25
    """
    # 检查输入视频文件是否存在
    if not os.path.exists(input_video_path):
        print(f"错误: 输入视频文件 '{input_video_path}' 不存在")
        return

    # 加载YOLOv8n模型
    model = YOLO('yolov8n.pt')  # 会自动下载模型（如果本地没有）
    # model = YOLO("yolo8n.pt")

    # 打开视频文件
    cap = cv2.VideoCapture(input_video_path)

    # 获取视频属性
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"视频信息: 宽度={frame_width}, 高度={frame_height}, FPS={fps}, 总帧数={total_frames}")

    # 初始化视频编写器（如果需要保存输出）
    out = None
    if output_video_path:
        # 获取输出目录并确保其存在
        output_dir = os.path.dirname(output_video_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 定义编解码器并创建VideoWriter对象
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 可以根据需要更改编解码器
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    # 处理视频帧
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # 视频处理完毕

        frame_count += 1
        if frame_count % 10 == 0:  # 每10帧打印一次进度
            print(f"处理中: {frame_count}/{total_frames} 帧 ({frame_count / total_frames * 100:.1f}%)")

        # 进行目标检测
        results = model(frame, conf=conf_threshold)

        # 获取带检测框的帧
        annotated_frame = results[0].plot()

        # 显示检测结果
        cv2.imshow('YOLOv8 视频检测', annotated_frame)

        # 保存检测结果（如果需要）
        if out:
            out.write(annotated_frame)

        # 按 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("用户中断处理")
            break

    # 释放资源
    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()
    print(f"处理完成，共处理 {frame_count} 帧")


if __name__ == "__main__":
    # 示例用法
    input_video = "001.mp4"  # 替换为你的输入视频路径
    output_video = "output_video.mp4"  # 替换为你的输出视频路径，或设为None不保存

    # 执行检测
    detect_video(
        input_video_path=input_video,
        output_video_path=output_video,
        conf_threshold=0.3  # 可以根据需要调整置信度阈值
    )
