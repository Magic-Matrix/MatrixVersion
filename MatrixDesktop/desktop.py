from MatrixDesktop.memu import Memeu
from MatrixDesktop.app import *

import cv2

image_names = [
    "home.jpg", "video.jpg", "draw.jpg", "keyboard.jpg"

]

class Desktop(object):
    def __init__(self):

        # 画布字典
        self.canvas = []

        self.memu = Memeu(image_names)

        self.main_canva = None

        self.memu_number = 0

        self.makeCanvas()

    def makeCanvas(self):

        self.canvas = [Canvas("Main"), VideoCanvas(), DrawCanvas(), KeyboardCanvas()]

        self.setMainCanvas(0)


    def addCanvas(self, canvas: Canvas):
        """
        加入画布
        :param canvas:
        :return:
        """
        name = canvas.getName()
        self.canvas.append(canvas)

        if len(self.canvas) == 1:
            self.setMainCanvas(0)

    # def getName(self):
    #     return list(self.canvas.keys())

    def setMainCanvas(self, index):
        self.main_canva = self.canvas[index]

    def __call__(self, image, point):
        """
        融合图片
        :param image: 需要融合的图片
        :return:
        """

        new_memu_number = self.clicked(point)

        if new_memu_number is not None:
            self.memu_number = new_memu_number



        canva_image = self.main_canva()

        # 添加菜单
        canva_image = self.memu.makeMemu(canva_image, self.memu_number)
        #
        # print(type(image[0,0,0]))
        # print(type(canva_image[0,0,0]))

        image = cv2.addWeighted(image, 1, canva_image, 0.8, 3)

        return image


    def clicked(self, point):

        # 菜单检查
        memu_click = self.memu.click(point)

        memu_number = None

        # print(memu_click)

        for tem in memu_click:
            if tem != -1:
                memu_number = tem
                break

        if memu_number is not None:
            self.memu_number = memu_number
            self.setMainCanvas(self.memu_number)

        self.main_canva.clicked(point)

        return memu_number



