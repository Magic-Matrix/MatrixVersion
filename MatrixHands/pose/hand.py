"""
手类
"""
import numpy as np


class Hand(object):
    def __init__(self, left_point: np.ndarray, right_point: np.ndarray):

        self.right_image_fingertip = None
        self.left_image_fingertip = None
        self.world_fingertip = None

        self.setImageFinger(left_point, right_point)


    def setImageFinger(self, left_point: np.ndarray, right_point: np.ndarray):
        self.left_image_fingertip = left_point[[4, 8, 12, 16, 20]]
        self.right_image_fingertip = right_point[[4, 8, 12, 16, 20]]

    def setWorldFinger(self, point: np.ndarray):

        if point.shape[1] == 4:
            self.world_fingertip = point[:, :-1]
        else:
            self.world_fingertip = point

    def getImageFinger(self, number=None):
        if number is None:
            return self.left_image_fingertip, self.right_image_fingertip
        else:
            return self.left_image_fingertip[number], self.right_image_fingertip[number]

    def getWorldFinger(self, number=None):
        if number is None:
            return self.world_fingertip
        else:
            return self.world_fingertip[number]









