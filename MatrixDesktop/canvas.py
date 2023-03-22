import numpy as np

class Canvas(object):
    def __init__(self, name):

        self.size = (720, 1280, 3)


        # 画布名称
        self.name = name

        self.clean()
        # self.video = np.ones(size, dtype="uint8")

        # ==========================================
        # 继承后需要修改

        # 有效区域
        # 左上角，右下角
        # x1, y1, x2, y2
        self.area = []

    def clean(self):
        """
        清空画布
        :return:
        """
        self.image = np.zeros(self.size, dtype="uint8")



    def draw(self):
        """
        更新图像，被继承之后就要重写
        :return:
        """

        return self.image


    def __call__(self):
        """
        返回画布图片
        :return:
        """


        return self.draw()

    def setName(self,name):
        """
        设置名字
        :param name:
        :return:
        """
        self.name = name
    def getName(self):
        """
        返回画布名字
        :return:
        """
        return self.name

    def clicked(self, point):
        """
        按下事件，继承后重写这部分
        :param point:
        :return:
        """

        pass

        # click = self.click(point)


    def click(self, point):
        """
        按下按钮检查区域
        :param point:
        :return: 返回一个列表，列表长度是按下的个数，元素是按下的区域编号
        """

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




