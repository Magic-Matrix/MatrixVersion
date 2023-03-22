
import time
class FPS(object):
    def __init__(self, number=5):
        """
        :param number: 默认5次取平均
        """

        # fps 列表
        self.fps = [0 for i in range(number)]

        # 上一次的时间
        self.last = 0

        self.number = number

    def __call__(self):
        # 获取当前时间
        now_time = time.time()

        # 计算当前的 fps
        fps = int(1 / (now_time - self.last))

        # 保留当前的时间
        self.last = now_time

        # 收录进列表
        self.fps.append(fps)

        # 移除开头的
        self.fps.pop(0)

        # 平均下来的 fps
        fps = sum(self.fps) // self.number

        return fps
