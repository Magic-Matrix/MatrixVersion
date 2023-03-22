
from MatrixDesktop.canvas import Canvas
import cv2
import numpy as np


class DrawCanvas(Canvas):
    def __init__(self):
        super(DrawCanvas, self).__init__("draw")

        self.pen_size = 5

        self.pen = None

        self.color = (0, 0, 255)

        self.clean_image = np.ones((50, 100, 3), dtype="uint8") * 255



    def draw(self):

        h, w = 200, 600
        self.image[h:h + 50, w:w + 100] = self.clean_image

        if self.pen is None:
            return self.image

        cv2.circle(self.image, self.pen, self.pen_size, self.color, self.pen_size+2)


        return self.image

    def clicked(self, point):
        """
        按下事件，继承后重写这部分
        :param point:
        :return:
        """



        if len(point) != 0:

            # 确定有按下
            # 获取第一个按下的手指
            self.pen = (int(point[0][0]), int(point[0][1]))

            # =================================================
            y, x = 200, 600

            # 取一个手指的坐标
            point_tem = point[0]

            x_l = [x, x + 100]
            y_l = [y, y + 100]


            if x_l[0] < point_tem[0] < x_l[1] and y_l[0] < point_tem[1] < y_l[1]:

                self.clean()

















