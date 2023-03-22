

import os
import numpy as np
import cv2
from MatrixHands.utils import loadData, saveData
from MatrixHands.camera.correct import RectifyDistort

# 块的分布
board = (11, 8)

# 每个块的宽度
size = 19.2


def cornerFind(image, size):
    """
    角点查找
    :param image: 图片
    :param size: 角点个数（横向个数，纵向个数）
    :return:
    """

    # 寻找
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    success, corners = cv2.findChessboardCorners(gray, size, None)

    if success:
        output = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        return output
    else:
        return None


if __name__ == "__main__":
    # 主动执行本文件的时候进行相机标定
    path = "../images/"

    left_path = path + "left/"
    right_path = path + "right/"

    left_image_list = os.listdir(left_path)
    right_image_list = os.listdir(right_path)

    left_image_list = [left_path + name for name in left_image_list]
    right_image_list = [right_path + name for name in right_image_list]

    # 双目相机信息文件
    double_path = "../data/double.pkl"


    if os.path.isfile(double_path):
        # 文件存在，读取
        datas = loadData(double_path)
        print(">", "double.pkl 文件加载成功！！")

    else:

        bw, bh = board

        objp = np.zeros((bw * bh, 3), np.float32)
        objp[:, :2] = np.mgrid[0:bw, 0:bh].T.reshape(-1, 2)
        objp *= size

        obj_points = []  # 存储标定板的坐标
        left_img_points = []  # 存储图片上的
        right_img_points = []  # 存储图片上的

        image_size = None

        for left_path, right_path in zip(left_image_list, right_image_list):

            # 读取图片
            left_image = cv2.imread(left_path)
            right_image = cv2.imread(right_path)

            image_size = left_image.shape[1::-1]

            left_corners = cornerFind(left_image, board)
            right_corners = cornerFind(right_image, board)

            if (left_corners is not None) and (right_corners is not None):

                # 添加一个标定板坐标
                obj_points.append(objp)

                # 添加一个图片坐标
                left_img_points.append(left_corners)
                right_img_points.append(right_corners)

                # 画出来
                cv2.drawChessboardCorners(left_image, board, left_corners, True)
                cv2.drawChessboardCorners(right_image, board, right_corners, True)
                cv2.circle(left_image, left_corners[0, 0].astype(int), 10, (255, 0, 0))
                cv2.circle(right_image, right_corners[0, 0].astype(int), 10, (255, 0, 0))

                # cv2.imwrite("left_image.jpg", left_image)

                # 显示出来
                cv2.imshow("left", left_image)
                cv2.imshow("right", right_image)
                cv2.waitKey(0)


            else:
                print("error: ", f"left: {type(left_corners)}     right: {type(right_corners)}")


        # 左相机标定
        _, l_mtx, l_dist, _, _ = cv2.calibrateCamera(obj_points, left_img_points, image_size, None, None)
        # 右相机标定
        _, r_mtx, r_dist, _, _  = cv2.calibrateCamera(obj_points, right_img_points, image_size, None, None)

        # print("\n>", "=" * 60)
        # print(">", "左相机内参矩阵：\n", l_mtx)
        # print(">", "左相机畸变参数：\n", l_dist)
        # print(">", "=" * 60)
        # print(">", "右相机内参矩阵：\n", l_mtx)
        # print(">", "右相机畸变参数：\n", l_dist)
        # print(">", "=" * 60+'\n')


        # 双目相机标定
        output = cv2.stereoCalibrate(
            obj_points,                             # 位置信息
            left_img_points, right_img_points,      # 左右图片的点
            l_mtx, l_dist,                 # 左内参矩阵、畸变参数
            r_mtx, r_dist,                 # 右内参矩阵、畸变参数
            image_size)

        ret, l_mtx, l_dist, r_mtx, r_dist, R, T, E, F = output

        datas = {
            "retval": ret,
            "leftCameraMatrix": l_mtx,
            "rightCameraMatrix": r_mtx,
            "leftDistCoeffs": l_dist,
            "rightDistCoeffs": r_dist,
            "R": R,
            "T": T,
            "E": E,
            "F": F,
        }

        saveData(double_path, datas)
        print(">", "double.pkl 文件已保存！！")

        print()
    print(">", "误差：", datas["retval"], "\n")
    print(">", "左相机内参矩阵：\n", datas["leftCameraMatrix"], "\n")
    print(">", "右相机内参矩阵：\n", datas["rightCameraMatrix"], "\n")
    print(">", "左相机畸变参数：\n", datas["leftDistCoeffs"], "\n")
    print(">", "右相机畸变参数：\n", datas["rightDistCoeffs"], "\n")

    print(">", "旋转矩阵：\n", datas["R"], "\n")
    print(">", "平移向量：\n", datas["T"], "\n")
    print(">", "E：\n", datas["E"], "\n")
    print(">", "F：\n", datas["F"], "\n")


    # ==================================================================
    # 去畸变测试

    # 加载图片（两张图片名字一样）
    image_name = "1632386283.967154.jpg"
    left_image = cv2.imread("../images/left/" + image_name)
    right_image = cv2.imread("../images/right/" + image_name)

    h, w, _ = left_image.shape

    # 实例化对象（去除畸变）
    rd = RectifyDistort((w, h), datas)

    # 分别去除左右的畸变
    left_new_image = rd(left_image, "left")
    right_new_image = rd(right_image, "right")

    # 两张旧图片（未去畸变）拼接
    image = np.hstack([left_image, right_image])

    # 两张新图片（去除畸变）拼接
    new_image = np.hstack([left_new_image, right_new_image])

    # 为了方便显示，就缩小原先图片的一半
    image = cv2.resize(image, (None, None), fx=0.5, fy=0.5)
    new_image = cv2.resize(new_image, (None, None), fx=0.5, fy=0.5)

    # 画线
    number = 10
    step = new_image.shape[0] // number
    for i in range(1, number):
        cv2.line(new_image, (0, step * i), (w * 2 - 1, step * i), (0, 255, 0))
        cv2.line(image, (0, step * i), (w * 2 - 1, step * i), (0, 0, 255))

    # cv2.imwrite("image.jpg", image)
    # cv2.imwrite("new_image.jpg", new_image)

    cv2.imshow("old_image", image)
    cv2.imshow("nem_image", new_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





