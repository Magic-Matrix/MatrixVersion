import cv2
import pickle
import numpy as np


def saveData(path: str, data: dict) -> None:
    """
    保存数据
    :param left_data: 左相机的数据
    :param right_data: 右相机的数据
    :return: 无
    """

    with open(path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


def loadData(path: str) -> dict:
    """
    读取数据
    :return: 是一个字典数据
    """
    # 读取路径

    with open(path, 'rb') as f:
        datas = pickle.load(f)

    return datas
