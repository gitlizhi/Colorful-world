#!/usr/bin/python
# -*- coding: utf-8 -*-
"""注: png格式压缩需安装pngquant包"""
import os
import base64
from PIL import Image
from hashlib import md5


class ImageCompression(object):
    """改变图像的尺寸和内存大小"""
    def get_size(self, file):
        # 获取文件大小:KB
        size = os.path.getsize(file)
        print(size)
        return size

    def get_outfile(self, infile, outfile):
        if outfile:
            return outfile
        dir, suffix = os.path.splitext(infile)
        outfile = '{}-out{}'.format(dir, suffix)
        return outfile

    def compress_image(self, infile, mb=4500, step=10, quality=95):
        """不改变图片尺寸压缩到指定大小
        :param infile: 压缩源文件
        :param outfile: 压缩文件保存地址
        :param mb: 压缩目标，KB
        :param step: 每次调整的压缩比率
        :param quality: 初始压缩比率
        :return: 压缩文件地址，压缩文件大小
        """
        o_size = self.get_size(infile)
        if o_size <= mb:
            return infile
        while o_size > mb:
            im = Image.open(infile)
            im.save(infile, quality=quality)
            if quality - step < 0:
                break
            quality -= step
            o_size = self.get_size(infile)

    def resize_image(self, infile):
        """修改图片尺寸
        :param infile: 图片源文件(同时也是新图片地址)
        :return:
        """
        im = Image.open(infile)
        x, y = im.size
        ratio = 4000/max(x, y)     # 设置最长边为4000px, 另外一边等比例缩小
        out = im.resize((int(x * ratio), int(y * ratio)), Image.ANTIALIAS)
        # outfile = self.get_outfile(infile, outfile)
        out.save(infile)

    def compression_png(self, filename):
        """对png图片进行压缩"""
        # --force
        cmd = "pngquant --force " + filename + " --quality 90 -o " + filename  # 压缩90%的质量，直接覆盖压缩至源文件
        os.system(cmd)
        if self.get_size(filename) > 4718592:
            self.compression_png(filename)


class CheckImage(object):
    """对图像继续检测: 分辨率 和 内存大小"""
    def check_resolution_ratio(self, img_path):
        """检测分辨率"""
        img = Image.open(img_path)
        x, y = img.size
        if max(x, y) > 4096:
            return False
        return True

    def check_memory(self, img_path):
        """检测内存大小"""
        with open(img_path, "rb") as f:
            size = len(base64.b64encode(f.read()))
            if size > 6291456:
                return False
            return True


def md5_data(path):
    """
    获取图片的md5值
    :param path: 图片路径
    :return: md5值
    """
    md = md5()
    img = open(path, 'rb')
    md.update(img.read())
    img.close()
    r = md.hexdigest()
    print(r)
    return r
