
"""
拍照脚本
"""


import cv2
from MatrixHands.camera.camera import Camera
import winsound
from MatrixHands.config import Config
import time


if __name__ == "__main__":

    # 视频对象
    left_camera = Camera(Config["double_camera"][0])
    right_camera = Camera(Config["double_camera"][1])


    # 预计拍照时间（负数，绝对值越大，第一张图片等待时间越长）
    count = -200

    # 拍摄间隔（越大，间隔越大）
    wait = 60

    while True:

        # 获取一帧图片，两张图片，一左一右
        left_image, right_image = left_camera(), right_camera()


        # 显示
        cv2.imshow("Left Video", left_image)
        cv2.imshow("Right Video", right_image)

        count += 1

        if count == 60:
            count = 0
            # 用当前的时间戳命名
            name = str(time.time()) + ".jpg"
            cv2.imwrite("../images/left/" + name, left_image)
            cv2.imwrite("../images/right/" + name, right_image)
            winsound.Beep(400, 300)
            print(name, "已保存")

        cv2.waitKey(1)
