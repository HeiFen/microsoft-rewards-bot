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
def ImageMatch(srctempl:str):
    # 截取当前画面
    shotSCreen()

    # 点击模板图片位置
    screenScale = 1
    src = r'.\screen-image\screen.jpg'
    target = cv2.imread(srctempl, cv2.IMREAD_GRAYSCALE)
    temp = cv2.imread(src, cv2.IMREAD_GRAYSCALE)

    theight, twidth = target.shape[:2]
    tempheight, tempwidth = temp.shape[:2]
    # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
    scaleTemp=cv2.resize(temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))
    stempheight, stempwidth = scaleTemp.shape[:2]
    # 匹配图片
    res = cv2.matchTemplate(scaleTemp, target, cv2.TM_CCOEFF_NORMED)
    mn_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if (max_val >= 0.9):
        # 计算出中心点
        top_left = max_loc
        bottom_right = (top_left[0] + twidth, top_left[1] + theight)
        tagHalfW=int(twidth/2)
        tagHalfH=int(theight/2)
        tagCenterX=top_left[0]+tagHalfW
        tagCenterY=top_left[1]+tagHalfH
        #左键点击屏幕上的这个位置
        pyautogui.click(tagCenterX,tagCenterY,button='left')
    
'''
Description: 搜索
return *
Author: LCY
'''    
def search(q:str):
    ImageMatch(r'.\click-img\search_input.png')

if __name__ == "__main__":
    search_list = ["q", "w", "e", "r"]
    # 打开浏览器
    os.system('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"')
    time.sleep(2)
    # 点击初始地址栏
    ImageMatch(r'.\click-img\search_start.png')
    
    # 开始循环搜索
    for search_val in search_list:
        pyautogui.typewrite(f"https://cn.bing.com/search?q={search_val}")
        time.sleep(1)
        pyautogui.press("enter")
        pyautogui.press("enter")
        time.sleep(3)
        shotSCreen()
        ImageMatch(r'.\click-img\search_input.png')
        time.sleep(3) # 等待3秒