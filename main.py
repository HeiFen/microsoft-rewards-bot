import pyautogui
import time
import datetime
import os
import cv2

# os.system('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"')

'''
Description: 截取当前画面
return *
Author: LCY
'''


def shotSCreen():
    image_dir = r"./screen-image"
    image_file = f"{image_dir}/screen.jpg"
    pyautogui.screenshot(image_file)


'''
Description: 点击指定图片位置
param * srctempl  
return *
Author: LCY
'''


def ImageMatch(srctempl: str):
    # 截取当前画面
    shotSCreen()

    screenScale = 1

    # 读取模板图像和屏幕截图图像
    target = cv2.imread(srctempl, cv2.IMREAD_GRAYSCALE)
    temp = cv2.imread(r'.\screen-image\screen.jpg', cv2.IMREAD_GRAYSCALE)

    tempheight, tempwidth = temp.shape[:2]
    # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
    scaleTemp = cv2.resize(
        temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))
    
    # 匹配图片
    res = cv2.matchTemplate(scaleTemp, target, cv2.TM_CCOEFF_NORMED)
    mn_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if (max_val >= 0.8):
        # 获取按钮图片的宽度和高度
        button_width, button_height = target.shape[::-1]

        # 计算按钮图片中心的坐标
        center_x = max_loc[0] + button_width // 2
        center_y = max_loc[1] + button_height // 2

        # 左键点击屏幕上的这个位置
        pyautogui.click(center_x, center_y, button='left')


'''
Description: 搜索
return *
Author: LCY
'''
def search(q: str):
    ImageMatch(r'.\click-img\search_input.png')


if __name__ == "__main__":
    search_list = ["q", "w", "e", "r"]
    # 打开浏览器
    os.system('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"')
    time.sleep(1)
    # 点击初始地址栏
    ImageMatch(r'.\click-img\search_start.png')

    # 开始PC循环搜索
    count = 0
    while count < 30:
        pyautogui.typewrite(f"https://cn.bing.com/search?q={count}")
        time.sleep(1)
        pyautogui.press("enter")
        pyautogui.press("enter")
        time.sleep(1)
        shotSCreen()
        ImageMatch(r'.\click-img\search_input.png')
        count += 1

    # 开始移动端循环搜索
    pyautogui.press("f12")
    ImageMatch(r'.\click-img\search_input.png')
    count = 30
    while count < 50:
        pyautogui.typewrite(f"https://cn.bing.com/search?q={count}")
        time.sleep(1)
        pyautogui.press("enter")
        pyautogui.press("enter")
        time.sleep(1)
        shotSCreen()
        ImageMatch(r'.\click-img\search_input.png')
        count += 1
