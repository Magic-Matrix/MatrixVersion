import cv2
import numpy as np
from MatrixHands.matrix_hands import MatrixHands
from MatrixHands.utils import saveData

"""
0: 大拇指
1: 食指
2: 中指
3: 无名指
4: 小拇指
"""
finger = 1


def drawPoint(image, point, color=None, r=15):
    if color is None:
        color = (0, 0, 255)

    point1 = (point[0] - r, point[1] - r)
    point2 = (point[0] + r, point[1] + r)
    cv2.line(image, point1, point2, color)

    point1 = (point[0] + r, point[1] - r)
    point2 = (point[0] - r, point[1] + r)
    cv2.line(image, point1, point2, color)

    r = (r // 3) * 2

    cv2.circle(image, point, r, color, 1)

    return image


def drawCircle(image, point, number=100, color=None, r=20):
    if color is None:
        color = (0, 0, 255)

    color2 = (0, 255, 0)

    end = (number / 100) * 360 - 90

    cv2.ellipse(image, point, (r, r), 0, -90, end, color2, 2)
    cv2.ellipse(image, point, (r, r), 0, end, 270, color, 2)

    return image


def choose_point(flag_point, hand_point, r=2):
    """
    判断是否选中了标志
    :param flag_point: 标志点
    :param hand_point: 手指点
    :param r: 半径
    :return:
    """

    l1 = (flag_point[0] - hand_point[0]) ** 2
    l2 = (flag_point[1] - hand_point[1]) ** 2

    l = (l1 + l2) ** 0.5

    if l < r:
        return True
    else:
        return False

def comput_distance(v1, v2):
    """
    计算欧式距离
    :param v1:
    :param v2:
    :return:
    """

    return sum((v1 - v2) ** 2) ** 0.5


def points3D_transform(points1, points2):
    """
    坐标转换
    https://blog.csdn.net/iamqianrenzhan/article/details/103464164
    :param points1: shape: (M, 3)
    :param points2: shape: (N, 3)
    :return:
    """

    # 计算出所有点的平均坐标
    # 转换前和转换后都要计算
    center_points1 = np.mean(points1, 0)
    center_points2 = np.mean(points2, 0)

    # 每个坐标减去平均值
    new_points1 = points1 - center_points1
    new_points2 = points2 - center_points2

    # 矩阵相乘，构造一个矩阵
    M = new_points2.T @ new_points1

    # 使用奇异值分解
    u, s, vt = np.linalg.svd(M)

    # 旋转矩阵
    R = u @ vt

    # 计算出行列式是否是负数
    if np.linalg.det(R) < 0:
        # 小数就反了
        R = -R

    # 反向计算出
    T = center_points2.T - (R @ center_points1)

    return R, T

if __name__ == "__main__":

    matrix_hand = MatrixHands("../data/double.pkl")

    # 获取图像尺寸
    w, h = matrix_hand.camera.size

    # 特征点位置列表
    flag_list = [
        # (w // 2, h // 2),                                       # 中心位置
        (w // 2 - 300, h // 2), (w // 2 + 300, h // 2),  # 左右点
        (w // 2, h // 2 + 150), (w // 2, h // 2 - 150)  # 上下点
    ]

    count = 0
    world_list = []

    all_world_list = []

    for flag_point in flag_list:

        while True:
            left, right, hand = matrix_hand()

            drawPoint(left, flag_point)

            # 如果检测到手就处理
            if len(hand) != 0:

                hand = hand[0]

                # 获取手的世界坐标和图像坐标
                world_point = hand.getWorldFinger(finger).astype(int)
                image_point, _ = hand.getImageFinger(finger)

                # 是否靠近
                if choose_point(flag_point, image_point):
                    # 靠近就自加
                    count += 1
                    # 添加一个世界坐标
                    world_list.append(world_point)

                # 画圆
                drawCircle(left, (image_point[0], image_point[1]), count * 2)

                # 超过 50 次就记录，并重新开始
                if count > 50:
                    count = 0

                    world_avg = np.mean(np.array(world_list), axis=0)


                    # 添加进世界坐标列表之中
                    all_world_list.append(world_avg)

                    # 清空
                    world_list = []

                    break

            cv2.imshow("left", left)
            # cv2.imshow("right", right)
            # cv2.imwrite("left.jpg", left)

            cv2.waitKey(1)

    world_matrix = np.array(all_world_list)

    # world_matrix = np.array([[162.68627451, -13.23529412, 406.],
    #           [-173.68627451, -13.62745098, 405.05882353],
    #           [-5.1372549, 71.78431373, 415.11764706],
    #           [-5.15686275, -96.25490196, 399.15686275]])

    # 欧氏距离
    x = comput_distance(world_matrix[0], world_matrix[1]) / 2
    y = comput_distance(world_matrix[2], world_matrix[3]) / 2

    # 最终的理想坐标
    world_matrix_output = np.array([
        [x, 0, 0],
        [-x, 0, 0],
        [0, y, 0],
        [0, -y, 0]])

    print(">", "world_matrix:\n", world_matrix, '\n')
    print(">", "world_matrix_output:\n", world_matrix_output, '\n')

    R, T = points3D_transform(world_matrix, world_matrix_output)

    print(">", "R:\n", R, '\n')
    print(">", "T:\n", T, '\n')

    transform = {"R": R, "T": T}

    saveData("../data/transform.pkl", transform)

