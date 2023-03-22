
# from MatrixHands.camera.camera import DoubleCamera
from MatrixHands.camera.thread_camera import DoubleCamera

from MatrixHands.pose.pose import DoublePose, ThreadDoublePose
from MatrixHands.camera.stereo3d import Stereo3D
import cv2

class MatrixHands(object):
    def __init__(self, path):

        # 双目相机
        self.camera = DoubleCamera(path)

        # 双目手势检测器
        self.pose = ThreadDoublePose()
        # self.pose = DoublePose()

        # 世界坐标预测
        self.stereo3D = Stereo3D(self.camera.Q)

    def __call__(self, draw=True):

        # 得到图像
        left, right = self.camera()

        # 检测出手的姿态
        left, right, left_output, right_output = self.pose(left, right, draw)

        output = self.stereo3D(left_output, right_output)

        return left, right, output






