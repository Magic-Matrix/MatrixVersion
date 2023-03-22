
"""
相机
"""

import cv2
from MatrixHands.config import Config
from MatrixHands.camera.correct import RectifyDistort
from MatrixHands.utils import loadData

class Camera(cv2.VideoCapture):
    def __init__(self, cam=0):
        super(Camera, self).__init__(cam)

        # 调节分辨率
        self.set(3, Config["width"])
        self.set(4, Config["height"])

    def __call__(self):
        """
        读取图片
        :return:
        """

        # 读取一帧图片
        ret, fram = self.read()

        # 确认是否获得图片
        if ret:

            return fram
        else:
            raise ValueError


class DoubleCamera(object):
    def __init__(self, path):

        # 双目
        self.left_camera = Camera(Config["double_camera"][0])
        self.right_camera = Camera(Config["double_camera"][1])

        # 获取双目相机的信息
        datas = loadData(path)

        # 图像宽高
        width = Config["width"]
        height = Config["height"]

        # 去除畸变
        self.rectify = RectifyDistort((width, height), datas)

        # Q矩阵
        self.Q = self.rectify.Q

        self.size = (width, height)


    def __call__(self):

        # 获取图片
        left_image = self.left_camera()
        right_image = self.right_camera()

        # 矫正
        left_rectify_image = self.rectify(left_image, "left")
        right_rectify_image = self.rectify(right_image, "right")

        return left_rectify_image, right_rectify_image
