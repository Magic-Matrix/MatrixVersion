import numpy as np

class Push(object):
    def __init__(self, number=10):

        self.number = number

    def __call__(self, hands):

        push_list = []

        for hand in hands:

            point = hand.getWorldFinger()

            # 对 z 坐标取绝对值
            z = abs(point[:, 2])

            # 是否在一定范围内
            push_hand = z < self.number

            push_list.append(push_hand)

        return push_list








