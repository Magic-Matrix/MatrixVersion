
import cv2
import numpy as np



class Memeu(object):
    def __init__(self, image_names):

        image_root_path = "./MatrixDesktop/texture/"

        self.images_list = []
        self.area = []

        for i, name in enumerate(image_names):

            image = cv2.imread(image_root_path + name)


            if image is None:
                continue

            self.images_list.append(image)

            side = i * 80
            x, y = 250, 100
            x1, y1, x2, y2 = x + side, y, x + 50 + side, y + 50

            self.area.append([x1, y1, x2, y2])

        self.area = np.array(self.area, dtype="uint16")


    def makeMemu(self, image, index=0):

        for i, tem in enumerate(self.images_list):

            if i == index:
                mark = tem > 50

                tem = np.array([255, 0, 255], dtype="uint16") * mark

            # 绘画
            x1, y1, x2, y2 = self.area[i]
            # print(x1, y1, x2, y2)
            image[y1:y2, x1:x2] = tem

        return image


    def click(self, point):

        area_tem = self.area.copy()

        if len(point) == 0:
            return []

        min_point = area_tem[:, :2]
        max_point = area_tem[:, 2:]

        point = np.array(point, dtype="uint16").reshape(-1, 1, 2)


        number = point.shape[0]

        min_point = np.array([min_point for i in range(number)], dtype="uint16")
        max_point = np.array([max_point for i in range(number)], dtype="uint16")
        # print(point.shape)
        # print(max_point.shape)


        mark1 = min_point < point

        mark2 = point < max_point

        mark = np.logical_and(mark1, mark2)

        mark = np.logical_and(mark[..., 0], mark[..., 1])
        # print(mark)

        click = []

        # 默认先后顺序：按照手指编号
        for tem in mark:
            if (np.sum(tem) != 0):
                # 这个手指按下特定区域的时候
                number = np.argmax(tem)

                click.append(number)

            else:
                click.append(-1)

        return click
