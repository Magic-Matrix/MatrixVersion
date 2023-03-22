"""
去除畸变、相机校正
"""

import cv2
import numpy as np


class RectifyDistort(object):
    def __init__(self, size: tuple, datas: dict):

        # 计算出立体矫正所需要的映射矩阵
        R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(
            datas["leftCameraMatrix"], datas["leftDistCoeffs"],
            datas["rightCameraMatrix"], datas["rightDistCoeffs"],
            size, datas["R"], datas["T"])


        self.Q = Q

        self.left_map = cv2.initUndistortRectifyMap(
            datas["leftCameraMatrix"],
            datas["leftDistCoeffs"],
            R1, P1, size, cv2.INTER_NEAREST)

        self.right_map = cv2.initUndistortRectifyMap(
            datas["rightCameraMatrix"],
            datas["rightDistCoeffs"],
            R2, P2, size, cv2.INTER_NEAREST)


    def __call__(self, image: np.ndarray, camera: str):
        """
        校正图
        :param image:
        :param camera: 摄像头区分
        :return:
        """

        if camera == "left":
            map1, map2 = self.left_map
        elif camera == "right":
            map1, map2 = self.right_map
        else:
            raise ValueError

        new_image = cv2.remap(image, map1, map2, cv2.INTER_LINEAR)

        return new_image


