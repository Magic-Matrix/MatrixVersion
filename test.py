import cv2
from MatrixHands import *
from MatrixDesktop import *


matrix = MatrixHands("./data/double.pkl")
coordinate = Coordinate("./data/transform.pkl")
fps_ = FPS()
push = Push()
desktop = Desktop()




while True:

    left, right, hand = matrix()

    # 纠正坐标系
    hand = coordinate(hand)
    push_point = []

    if len(hand) != 0:

        push_list = push(hand)

        hand = hand[0]
        push_list = push_list[0]

        for i in range(5):

            point = hand.getWorldFinger(i).astype(int)
            l_point, r_point = hand.getImageFinger(i)

            push_finger = push_list[i]

            if push_finger:
                cv2.circle(left, (l_point[0], l_point[1]), 10, (0, 255, 0), 2)

                push_point.append(l_point[:-1])
            else:
                cv2.circle(left, (l_point[0], l_point[1]), 10, (0, 0, 255), 2)

            # 显示手指上的坐标
            # cv2.putText(left, f"{point}", (l_point[0], l_point[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            # cv2.putText(left, f"    {point[2]}", (l_point[0], l_point[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)



    image = desktop(left, push_point)



    # cv2.circle(left, (left.shape[1] // 2, left.shape[0] // 2), 5, (0, 0, 255), 2)
    fps = fps_()
    # cv2.putText(image, f"FPS: {fps}", (40, 40),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("left", image)
    # cv2.imshow("left", left)
    # cv2.imshow("right", right)

    cv2.imwrite("left.jpg", image)

    cv2.waitKey(1)





