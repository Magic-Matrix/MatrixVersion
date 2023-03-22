
from MatrixHands.utils import loadData
from MatrixHands.config import Config
from MatrixHands.camera.correct import RectifyDistort
from threading import Thread
import cv2
import time


class Camera(object):
    """
    多线程相机
    """
    def __init__(self, src, name):
        # 摄像头
        self.capture = cv2.VideoCapture(src)
        self.name = name

        # 调节分辨率
        self.capture.set(3, Config["width"])
        self.capture.set(4, Config["height"])

        # 测试一下
        self.ret, self.frame = self.capture.read()

        # 线程
        self.thread = Thread(target=self.update, args=())

        # 主线程结束，子线程也结束
        self.thread.daemon = True

    def setRectify(self, rectify):
        """
        添加矫正器
        :param rectify: 矫正器
        :return:
        """
        self.rectify = rectify

    def rectifyImage(self, image):
        """
        矫正图片
        :param image:
        :return:
        """
        image = self.rectify(image, self.name)

        return image

    def start(self):
        """
        开启线程
        :return:
        """
        self.thread.start()

    def update(self):
        """
        更新
        :return:
        """
        while True:

            ret, frame = self.capture.read()

            if ret:
                # 矫正
                frame = self.rectifyImage(frame)

                self.frame = frame
                self.ret = ret

            time.sleep(.01)

    def read(self):
        return self.ret, self.frame.copy()

class DoubleCamera(object):
    def __init__(self, path):

        # 双目
        self.left_camera = Camera(Config["double_camera"][0], "left")
        self.right_camera = Camera(Config["double_camera"][1], "right")

        # 获取双目相机的信息
        datas = loadData(path)

        # 图像宽高
        width = Config["width"]
        height = Config["height"]

        # 去除畸变
        rectify = RectifyDistort((width, height), datas)

        # Q矩阵
        self.Q = rectify.Q

        self.size = (width, height)

        self.left_camera.setRectify(rectify)
        self.right_camera.setRectify(rectify)

        self.start()

    def start(self):
        self.left_camera.start()
        self.right_camera.start()

    def read(self):
        left_ret, left_image = self.left_camera.read()
        right_ret, right_image = self.right_camera.read()

        ret = left_ret and right_ret

        return ret, left_image, right_image


    def __call__(self):

        # 获取图片
        _, left_image, right_image = self.read()

        return left_image, right_image