
from MatrixHands.pose.hand import Hand
import cv2
import numpy as np


class Stereo3D(object):
    def __init__(self, Q: np.ndarray):

        self.Q = Q

        # 指定的点
        self.point_list = [4, 8, 12, 16, 20]

    def worldPosition(self, hand: Hand):
        """
        计算世界坐标
        :param left_hand: 左图手
        :param right_hand: 右图手
        :return:
        """


        # 得到手的坐标  (5, 3)
        left_point, right_point = hand.getImageFinger()

        # 转置过来，方便计算
        left_point = left_point.T
        right_point = right_point.T

        finger_number = left_point.shape[1]

        x, y, z = left_point

        x_r, y_r, z_r = right_point

        loss = sum(abs(y_r - y)) / finger_number

        if loss > 50:
            # 不匹配情况，直接返回空
            return None

        # 计算视察
        d = abs(x - x_r)

        one = np.ones(finger_number, dtype=int)

        # shape: (4, 21)
        points = np.array([x, y, d, one])

        output = np.dot(self.Q, points)

        w = output[3]

        hand.setWorldFinger((output / w).T)

        return hand

    def __call__(self, left_hands: list, right_hands: list):
        """
        左右图像中的手进行匹配
        :param left_hands:
        :param right_hands:
        :return:
        """
        # 有一个没有检查出手的图片就直接退出
        if len(left_hands) == 0 or len(right_hands) == 0:
            return []

        left_points = left_hands[0]
        right_points = right_hands[0]

        # 实例化 手
        hand = Hand(left_points, right_points)

        output = self.worldPosition(hand)

        if output is None:
            return []
        else:
            return [output]