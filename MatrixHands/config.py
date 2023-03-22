
Config = {

    # 视频分辨率
    "height": 720,
    "width": 1280,

    # 双摄像头编号: 左，右
    "double_camera": [0, 1],

    # 最多手的数量
    "max_num_hands": 1,

    # 最小检测置信度，用于目标检测
    "min_detection_confidence": 0.5,

    # 最小追踪置信度，低于这个值就会重新目标检测
    "min_tracking_confidence": 0.5,
}