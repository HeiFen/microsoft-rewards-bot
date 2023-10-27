import pyautogui
import time
import os
import cv2
import random
import winreg
import atexit

INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\Microsoft\Windows\CurrentVersion\Internet Settings', 0, winreg.KEY_ALL_ACCESS)
proxy_status, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, 'ProxyEnable')

def setProxyStatus(value):
    winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyEnable', 0, reg_type, value)

def shotSCreen():
    image_dir = r"./screen-image"
    image_file = f"{image_dir}/screen.jpg"
    pyautogui.screenshot(image_file)

def imageMatch(srctempl: str):
    # 截取当前画面
    shotSCreen()

    screenScale = 1

    # 读取模板图像和屏幕截图图像
    target = cv2.imread(srctempl)
    temp = cv2.imread(r'.\screen-image\screen.jpg')

    tempheight, tempwidth = temp.shape[:2]
    # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
    scaleTemp = cv2.resize(
        temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))

    # 匹配图片
    res = cv2.matchTemplate(scaleTemp, target, cv2.TM_CCOEFF_NORMED)
    mn_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_val >= 0.8

def imageClick(srctempl: str):
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
    
def autoSearch(count: int):
    index = 0
    while index < count:
        imageClick(r'.\click-img\search_input.png')
        search = random.randint(0, 999999999)
        pyautogui.typewrite(f"https://cn.bing.com/search?q={search}")
        time.sleep(3)
        pyautogui.press("enter")
        pyautogui.press("enter")
        time.sleep(3)
        index += 1

if __name__ == "__main__":
    # 获取代理，如果代理是开启状态，需要先关闭代理进行搜索，然后脚本结束重新开启代理
    if (proxy_status == 1):
        # 关闭代理
        setProxyStatus(0)
        # 设置脚本结束重新打开代理
        atexit.register(setProxyStatus, 1)

    # 打开浏览器
    os.system('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"')
    time.sleep(1)

    # 开始PC循环搜索
    autoSearch(34)

    # 转换到移动端
    pyautogui.press("f12")
    time.sleep(1)
    if (imageMatch(r'.\click-img\if-phone.png') == False):
        imageClick(r'.\click-img\f12-off.png')
    time.sleep(1)

    # 开始移动端循环搜索
    autoSearch(21)
