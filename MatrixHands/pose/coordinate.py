import numpy as np
import math
from MatrixHands.utils import loadData


def sin(alpha):
    return math.sin(alpha)


def cos(alpha):
    return math.cos(alpha)


class Coordinate(object):
    def __init__(self, path=None):

        if path is not None:
            data = loadData(path)
            self.R = data["R"]
            self.T = data["T"].reshape(3, 1)
            return

        # 平移向量
        self.T = np.array([[-5], [-17], [430]])

        # 旋转角度
        x_angle = math.pi
        y_angle = math.pi/ 200
        z_angle = 0

        # 围绕 X 轴旋转
        X = np.array([
            [1, 0, 0],
            [0, cos(x_angle), sin(x_angle)],
            [0, -sin(x_angle), cos(x_angle)]
        ])

        # 围绕 Y 轴旋转
        Y = np.array([
            [cos(y_angle), 0, -sin(y_angle)],
            [0, 1, 0],
            [sin(y_angle), 0, cos(y_angle)]
        ])

        # 围绕 Z 轴旋转
        Z = np.array([
            [cos(z_angle), -sin(y_angle), 0],
            [sin(y_angle), cos(z_angle), 0],
            [0, 0, 1]
        ])

        # 整合成旋转矩阵
        self.R = np.dot(X, Y, Z)


    def change(self, point: np.ndarray):
        """
        转换坐标系
        :param point: 坐标点，必须是（3, N）才行
        :return:
        """

        # 判断形状
        if point.shape[0] != 3:
            raise ValueError("shape is wrong")

        output = np.dot(self.R, point) + self.T

        return output


    def __call__(self, hands):

        for hand in hands:
            # 获取世界坐标
            point = hand.getWorldFinger().T

            # 坐标系转换
            point = self.change(point).T

            # 重新更新坐标数据
            hand.setWorldFinger(point)

        return hands


