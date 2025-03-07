
import random
import time
import cv2
import numpy as np
import pyautogui
import os
from helper.helper import human_click, imageClick, openUrl, shotSCreen


def autoActivity():
    # 进入首页
    openUrl("https://rewards.bing.com/")
    time.sleep(5)
    
    # 记录已点击过的位置，避免重复点击
    clicked_positions = set()
    
    # 设置最大滚动次数，防止无限循环
    max_scroll_count = 10
    scroll_count = 0
    
    # 连续没有找到新按钮的次数
    no_new_buttons_count = 0
    
    # 检查模板图像是否存在
    template_path = r'.\clickImg\activity_on.png'
    if not os.path.exists(template_path):
        print(f"错误：模板图像不存在: {template_path}")
        return
    
    print("开始查找并点击活动按钮...")
    
    while scroll_count < max_scroll_count and no_new_buttons_count < 2:
        # 获取当前屏幕上所有可点击活动
        shotSCreen()
        print(f"第 {scroll_count + 1} 次扫描屏幕")

        screenScale = 1

        # 读取模板图像和屏幕截图图像
        target = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        temp = cv2.imread(r'.\screen-image\screen.jpg', cv2.IMREAD_GRAYSCALE)

        if target is None or temp is None:
            print("错误：无法读取模板图像或屏幕截图")
            time.sleep(1)
            continue

        tempheight, tempwidth = temp.shape[:2]
        target_height, target_width = target.shape[:2]
        print(f"屏幕尺寸: {tempwidth}x{tempheight}, 模板尺寸: {target_width}x{target_height}")
        
        # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
        scaleTemp = cv2.resize(
            temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))

        # 匹配图片
        res = cv2.matchTemplate(scaleTemp, target, cv2.TM_CCOEFF_NORMED)
        # 设置阈值 - 稍微降低阈值以提高匹配率
        threshold = 0.75
        loc = np.where(res >= threshold)

        # 获取按钮图片的宽度和高度
        button_width, button_height = target.shape[::-1]

        # 存储所有匹配的位置
        matches = []
        for pt in zip(*loc[::-1]):
            matches.append(pt)
            # 打印每个初始匹配位置的详细信息
            print(f"初始匹配位置: ({pt[0]}, {pt[1]}), 匹配值: {res[pt[1]][pt[0]]:.4f}")

        print(f"找到 {len(matches)} 个初始匹配位置")

        # 去重处理 - 增加距离阈值以更好地区分不同按钮
        unique_matches = []
        for match in matches:
            # 检查匹配质量，过滤掉低质量匹配
            match_quality = res[match[1]][match[0]]
            if match_quality < 0.8:  # 提高质量要求
                print(f"过滤低质量匹配: ({match[0]}, {match[1]}), 匹配值: {match_quality:.4f}")
                continue
                
            # 检查是否与已有匹配过近
            is_duplicate = False
            for x in unique_matches:
                distance = ((match[0] - x[0])**2 + (match[1] - x[1])**2)**0.5
                if distance < 20:  # 增加距离阈值
                    is_duplicate = True
                    print(f"过滤重复匹配: ({match[0]}, {match[1]}), 与({x[0]}, {x[1]})距离为{distance:.2f}")
                    break
                    
            if not is_duplicate:
                unique_matches.append(match)
                print(f"保留有效匹配: ({match[0]}, {match[1]}), 匹配值: {match_quality:.4f}")
        
        print(f"去重后剩余 {len(unique_matches)} 个匹配位置")
        
        # 记录本次找到的新按钮数量
        new_buttons_found = 0
        
        # 验证匹配位置的合理性
        valid_matches = []
        screen_width, screen_height = pyautogui.size()
        
        for match in unique_matches:
            center_x = match[0] + button_width // 2
            center_y = match[1] + button_height // 2
            
            # 检查位置是否在屏幕范围内且不在边缘
            if (center_x > 50 and center_x < screen_width - 50 and 
                center_y > 50 and center_y < screen_height - 50):
                valid_matches.append(match)
            else:
                print(f"过滤无效位置: ({center_x}, {center_y}) - 超出有效屏幕范围")
        
        print(f"验证后剩余 {len(valid_matches)} 个有效位置")
        
        # 点击所有有效匹配的位置
        for i, match in enumerate(valid_matches):
            # 计算按钮图片中心的坐标
            center_x = match[0] + button_width // 2
            center_y = match[1] + button_height // 2
            
            # 检查是否已经点击过该位置 - 使用更大的容差范围
            already_clicked = False
            for pos in clicked_positions:
                pos_x, pos_y = map(int, pos.split('_'))
                if abs(center_x - pos_x) < 20 and abs(center_y - pos_y) < 20:
                    already_clicked = True
                    break
            
            position_key = f"{center_x}_{center_y}"
            if not already_clicked:
                print(f"点击新按钮 #{i+1}: 位置({center_x}, {center_y})")
                clicked_positions.add(position_key)
                new_buttons_found += 1
                
                # 点击按钮
                human_click(center_x, center_y)
                time.sleep(3)
                pyautogui.hotkey('ctrl', 'w')  # 关闭标签页
                time.sleep(2)  # 增加等待时间
            else:
                print(f"跳过已点击过的按钮: 位置({center_x}, {center_y})")
        
        # 如果没有找到新按钮，增加计数器
        if new_buttons_found == 0:
            no_new_buttons_count += 1
            print(f"本次未找到新按钮，连续 {no_new_buttons_count} 次未找到")
        else:
            # 如果找到了新按钮，重置计数器
            no_new_buttons_count = 0
            print(f"本次找到 {new_buttons_found} 个新按钮")
        
        # 向下滚动页面
        print("向下滚动页面...")
        pyautogui.scroll(-1000)  # 负值表示向下滚动
        time.sleep(2.5)  # 增加等待时间，确保页面完全加载
        scroll_count += 1
        
    print(f"完成所有活动点击，共滚动{scroll_count}次，点击了{len(clicked_positions)}个活动按钮")
