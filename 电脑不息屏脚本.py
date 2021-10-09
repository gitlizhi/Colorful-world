#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
原理: 通过控制鼠标的移动, 使电脑保持清醒状态
"""
# 导入相关库
import pyautogui
import random
import time

# 使用while True循环，让程序一直执行！
while True:
    x = random.randint(-200, 200)
    y = random.randint(-200, 200)
    pyautogui.moveRel(x, y)
    pyautogui.click()
    time.sleep(5)  # 让鼠标移动到某个位置，停留几秒钟，我怕它太累

