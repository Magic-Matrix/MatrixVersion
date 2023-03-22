
from MatrixDesktop.canvas import Canvas
import cv2
import numpy as np


class VideoCanvas(Canvas):
    def __init__(self):
        super(VideoCanvas, self).__init__("video")


        self.area = [[]]

        # 移动按钮
        self.setMoveButton(300, 200)

        image = cv2.imread("./MatrixDesktop/texture/move.jpg")

        self.image_move = cv2.resize(image, (30, 30))

        self.area = np.array(self.area, dtype="uint16")

        self.video = cv2.VideoCapture("./MatrixDesktop/app/video/video.mp4")

        self.image_size = (640, 360)


    def setMoveButton(self, x, y):
        self.area[0] = [x, y, x + 30, y + 30]


    def draw(self):

        image = self.image.copy()
        # 获取视频的一帧
        success, image_video = self.video.read()


        if success:
            # 检查移动坐标
            x1, y1, x2, y2 = self.area[0]

            # 计算大小
            x1, y1 = (x1 + x2) // 2, (y1 + y2) // 2
            x2, y2 = x1 + self.image_size[0], y1 + self.image_size[1]

            # 缩放
            image_video = cv2.resize(image_video, self.image_size)

            # 替换掉，换成视频
            image[y1:y2, x1:x2] = image_video


        # 替换掉，换成移动按钮
        x1, y1, x2, y2 = self.area[0]

        image[y1:y2, x1:x2] = self.image_move

        return image

    def clicked(self, point):

        click = self.click(point)

        # 如果按下了移动按键
        if 0 in click:

            # 获取按下按钮的手指索引
            index = click.index(0)

            # 获取按下按钮的手指坐标
            index_point = point[index]

            self.setMoveButton(index_point[0] - 15, index_point[1] - 15)



        








