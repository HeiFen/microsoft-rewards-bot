import subprocess
import time
import os

import pyautogui
from func.activity import autoActivity
from func.search import autoSearch
from helper import helper
from helper.helper import check_proxy_status, setProxyStatus
from playwright.sync_api import sync_playwright


if __name__ == "__main__":

    ORIGIN_PROXY_STATUS = check_proxy_status()

    # 关闭代理
    if (ORIGIN_PROXY_STATUS == True):
        setProxyStatus(False)

    # 打开浏览器
    edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    subprocess.Popen([edge_path, '--start-maximized'])
    time.sleep(1)
    # 全屏
    helper.imageClick(r'.\clickImg\maximize.png')

    # 开始PC搜索循环搜索
    autoSearch(34)

    # 点击奖励活动
    autoActivity()
    
    # 关闭浏览器
    pyautogui.hotkey('alt', 'f4')  # Windows/Linux

    # 还原代理状态
    now_proxy_status = check_proxy_status()
    if now_proxy_status != ORIGIN_PROXY_STATUS:
        setProxyStatus(ORIGIN_PROXY_STATUS)
