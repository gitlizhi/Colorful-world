#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
该OCR识别是一个用于识别验证码的开源库，又名带带弟弟ocr，爬虫界大佬sml2h3开发，识别效果也是非常不错，对一些常规的数字、字母验证码识别有奇效。
安装库: pip install ddddocr -i https://pypi.tuna.tsinghua.edu.cn/simple
"""
import ddddocr

ocr = ddddocr.DdddOcr()
with open('图片路径', 'rb') as f:
    img_bytes = f.read()
res = ocr.classification(img_bytes)
print(res)
