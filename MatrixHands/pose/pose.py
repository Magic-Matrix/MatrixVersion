
from MatrixHands.config import Config
import mediapipe as mp
import cv2
import numpy as np


class Pose(object):
    def __init__(self):

        # 检测器
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=Config["max_num_hands"],
            min_detection_confidence=Config["min_detection_confidence"],
            min_tracking_confidence=Config["min_tracking_confidence"])

        self.draw = mp.solutions.drawing_utils

        # 保存宽度和高度
        self.width = Config["width"]
        self.height = Config["height"]

        # 制作一个向量
        self.size = np.array([self.width, self.height, self.width])


    def __call__(self, image, flag=True):

        # 颜色转换
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 输出识别结果
        results = self.hands.process(imageRGB)

        output = []

        if results.multi_hand_landmarks:

            # 针对每个点进行遍历

            # print(result, len(result.multi_hand_landmarks))

            for landmark, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):

                # 识别左右手，不太准
                # print(handedness)

                # 每个手的信息
                # shape: (21, 3)
                hand = np.array([[lm.x, lm.y, lm.z] for lm in landmark.landmark])

                # 恢复成正常的数据
                hand = (hand * self.size).astype(int)

                # 添加进来
                output.append(hand)

                if flag:

                    self.draw.draw_landmarks(
                        image, landmark, mp.solutions.hands.HAND_CONNECTIONS,
                        mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                        mp.solutions.drawing_styles.get_default_hand_connections_style())

        return image, output




class DoublePose(object):
    def __init__(self):
        self.pose_left = Pose()
        self.pose_right = Pose()

    def __call__(self, left_image, right_image, flag):
        left_image, left_output = self.pose_left(left_image, flag)
        right_image, right_output = self.pose_right(right_image, flag)

        return left_image, right_image, left_output, right_output


from concurrent.futures import ThreadPoolExecutor, as_completed


class ThreadDoublePose(object):
    """
    子线程检测器
    """
    def __init__(self):

        self.left_pose = Pose()
        self.right_pose = Pose()

        # 创建线程池，最多两个线程
        self.pool = ThreadPoolExecutor(2)

    def function(self, name, image, flag):

        if name == "left":
            function = self.left_pose.__call__
        else:
            function = self.right_pose.__call__

        output = function(image, flag)



        return name, output


    def setPose(self, name, image, flag):
        """
        将任务添加到线程池
        :param name: 手的名字
        :param image: 图片
        :param flag: 是否显示
        :return:
        """

        task = self.pool.submit(self.function, name, image, flag)

        return task

    def __call__(self, left_image, right_image, flag):

        task_list = [
            self.setPose("left", left_image, flag),
            self.setPose("right", right_image, flag)
        ]

        out_dict = {}

        for tem in as_completed(task_list):
            name, output = tem.result()

            out_dict[name] = output

        left_image, left_output = out_dict["left"]
        right_image, right_output = out_dict["right"]

        return left_image, right_image, left_output, right_output


















