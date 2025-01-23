
import random
import time

import pyautogui
import pyperclip
from helper.helper import imageClick

def autoSearch(count: int):
    index = 0
    while index < count:
        # 点击
        imageClick(r'.\clickImg\search_input.png')
        time.sleep(1)
        # 搜索词放在剪贴板
        search1 = chr(random.randint(0x4e00, 0x9fbf))
        search2 = chr(random.randint(0x4e00, 0x9fbf))
        search3 = chr(random.randint(0x4e00, 0x9fbf))
        search4 = chr(random.randint(0x4e00, 0x9fbf))
        search5 = chr(random.randint(0x4e00, 0x9fbf))
        # pyperclip.copy(f"https://www.bing.com/search?q={search1 + search2 + search3 + search4 + search5}&cvid=175ed9bf25dd4da9a00a62f37680aea1&gs_lcrp=EgRlZGdlKgYIABBFGDkyBggAEEUYOTIGCAEQABhA0gEHOTIzajBqNKgCCLACAQ&FORM=ANAB01&PC=U531")
        pyperclip.copy(f"{search1 + search2 + search3 + search4 + search5}")

        # 粘贴在搜索栏
        pyautogui.hotkey('Ctrl', 'V')
        time.sleep(3)
        pyautogui.press("enter")
        pyautogui.press("enter")
        time.sleep(3)
        index += 1

