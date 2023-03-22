
"""
相机
"""

import cv2
import pickle
import numpy as np

def loadData(path: str) -> dict:
    """
    读取数据
    :return: 是一个字典数据
    """
    # 读取路径

    with open(path, 'rb') as f:
        datas = pickle.load(f)

    return datas

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



if __name__ == "__main__":


    # 标注文件路径（根据自己路径去修改）
    path = "D:/Project/Python/MatrixVision/data/double.pkl"
    # 选择一个相机，可以填 "left" 或 "right"
    camera = "left"

    # ======================================================================

    # 获取双目相机的标注文件
    datas = loadData(path)

    cap = cv2.VideoCapture(0)

    # 相机采集图像尺寸调整
    width = 1280
    height = 720
    cap.set(3, width)
    cap.set(4, height)

    rectify = RectifyDistort((width, height), datas)

    while True:
        ret, fram = cap.read()

        if not ret:
            print("无法打开相机，自动退出")
            exit()

        # 畸变矫正
        fram = rectify(fram, camera)

        cv2.imshow("image", fram)
        cv2.waitKey(1)



