

import random
import winreg
import cv2
import pyautogui
import pyperclip


INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\Microsoft\Windows\CurrentVersion\Internet Settings', 0, winreg.KEY_ALL_ACCESS)
proxy_status, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, 'ProxyEnable')

def setProxyStatus(value):
    winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyEnable', 0, reg_type, value)


def check_proxy_status():
    try:
        # 打开注册表项
        INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                           r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                           0,
                                           winreg.KEY_READ)

        # 获取 ProxyEnable 的值
        proxy_status, reg_type = winreg.QueryValueEx(
            INTERNET_SETTINGS, 'ProxyEnable')

        # 关闭注册表项
        winreg.CloseKey(INTERNET_SETTINGS)

        return proxy_status == 1
    except Exception as e:
        print(f"检查代理状态时出错: {e}")
        return False


def shotSCreen():
    image_dir = r"./screen-image"
    image_file = f"{image_dir}/screen.jpg"
    pyautogui.screenshot(image_file)

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
        human_click(center_x, center_y)


def human_click(x, y):
    # 随机移动路径点击
    # current_x, current_y = pyautogui.position()
    # steps = random.randint(5, 10)
    # for i in range(steps):
    #     target_x = current_x + (x - current_x) * (i + 1) / steps
    #     target_y = current_y + (y - current_y) * (i + 1) / steps
    #     pyautogui.moveTo(target_x, target_y)
    # pyautogui.leftClick()

    # 直接点击
    pyautogui.moveTo(x, y, 0.3)
    pyautogui.leftClick()



def openUrl(url: str): 
    # 鼠标点击搜索栏
    imageClick(r'.\clickImg\search_input.png')
    # 输入网址
    pyperclip.copy(url)
    pyautogui.hotkey('Ctrl', 'V')
    pyautogui.press("enter")
    pyautogui.press("enter")