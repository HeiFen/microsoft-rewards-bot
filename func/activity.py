
import random
import time
import cv2
import numpy as np
import pyautogui
from helper.helper import human_click, imageClick, openUrl, shotSCreen


def autoActivity():
    # 进入首页
    openUrl("https://rewards.bing.com/")
    time.sleep(5)
    # 获取所有可点击活动
    shotSCreen()

    screenScale = 1

    # 读取模板图像和屏幕截图图像
    target = cv2.imread(r'.\clickImg\activity_on.png', cv2.IMREAD_GRAYSCALE)
    temp = cv2.imread(r'.\screen-image\screen.jpg', cv2.IMREAD_GRAYSCALE)

    tempheight, tempwidth = temp.shape[:2]
    # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
    scaleTemp = cv2.resize(
        temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))

    # 匹配图片
    res = cv2.matchTemplate(scaleTemp, target, cv2.TM_CCOEFF_NORMED)
    # 设置阈值
    threshold = 0.8
    loc = np.where(res >= threshold)

    # 获取按钮图片的宽度和高度
    button_width, button_height = target.shape[::-1]

    # 存储所有匹配的位置
    matches = []
    for pt in zip(*loc[::-1]):
        matches.append(pt)

    # 去重处理
    unique_matches = []
    for match in matches:
        if not any(abs(match[0] - x[0]) < 10 and abs(match[1] - x[1]) < 10 for x in unique_matches):
            unique_matches.append(match)

    # 打印所有匹配的位置
    for match in unique_matches:
        # 计算按钮图片中心的坐标
        center_x = match[0] + button_width // 2
        center_y = match[1] + button_height // 2
        human_click(center_x, center_y)
        time.sleep(3)
        pyautogui.hotkey('ctrl', 'w')  # Windows/Linux
        time.sleep(random.uniform(0.1, 0.3))
