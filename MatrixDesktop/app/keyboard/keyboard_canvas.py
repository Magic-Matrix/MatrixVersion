
from MatrixDesktop.canvas import Canvas
import cv2
import numpy as np


class KeyboardCanvas(Canvas):
    def __init__(self):
        super(KeyboardCanvas, self).__init__("keyboard")

        keyboard_image = cv2.imread("./MatrixDesktop/texture/keyboard.jpeg")

        keyboard_image = cv2.resize(keyboard_image, (None, None), fx=0.4, fy=0.4)

        x, y = 200, 200

        x1, y1, x2, y2 = x, y, x + 336, y + 336

        self.image[y1:y2, x1:x2] = keyboard_image

        self.numbers = ""

        self.area = [
            [370, 255],
            [290, 330], [370, 330], [450, 330],
            [290, 405], [370, 405], [450, 405],
            [290, 480], [370, 480], [450, 480]
        ]


    def putTxext(self, text:str):

        length = len(text)

        row = length // 10

        str_list = []


        j = 0

        for i in range(row):
            str_list.append(text[i*10:(i+1)*10])
            j += 1


        str_list.append(text[j*10:])

        for i, tem in enumerate(str_list):
            cv2.putText(self.image, tem, (600, 250 + i * 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)


    def draw(self):
        """
        更新图像，被继承之后就要重写
        :return:
        """

        if self.numbers != "":
            self.putTxext( self.numbers)


        return self.image

    def click(self, point):
        area_tem = np.array(self.area, dtype="uint16")

        if len(point) == 0:
            return None

        # 取一个手指的坐标
        point = point[0]

        length = area_tem - point

        # 计算出距离
        length = ((length[:, 0] ** 2) + (length[:, 1] ** 2)) ** 0.5

        number = np.argmin(length)

        return number


    def clicked(self, point):


        click = self.click(point)

        if click is None:
            return

        self.numbers += str(click)


