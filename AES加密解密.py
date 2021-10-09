#!/usr/bin/python
# -*- coding: utf-8 -*-
import base64
from Crypto.Cipher import AES

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class Aes(object):
    """AES对称加密算法之ECB模式"""
    def __init__(self):
        self.__key = 'gXCue61haIvwse6xGbBocnCyXeQ='  # 密钥(可自己生成, 存在安全的位置, 为了方便测试写死在这里)

    @classmethod
    def add_to_32(cls, value):
        while len(value) % 32 != 0:
            value += '\0'
        return str.encode(value)  # 返回bytes

    @classmethod
    def add_to_16(cls, value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)  # 返回bytes

    def encrypt_oracle(self, text):
        """加密过程"""
        # 初始化加密器
        aes = AES.new(self.add_to_16(self.__key), AES.MODE_ECB)  #
        # 先进行aes加密
        encrypt_aes = aes.encrypt(self.add_to_16(pad(text)))
        # 用base64转成字符串形式
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
        return encrypted_text

    def decrypt_oralce(self, text):
        """解密过程"""
        # 初始化加密器
        aes = AES.new(self.add_to_16(self.__key), AES.MODE_ECB)  # self.add_to_16(self.__key)
        # 优先逆向解密base64成bytes
        base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
        # 执行解密密并转码返回str
        decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')
        return unpad(decrypted_text)


if __name__ == '__main__':

    str_data = 'ABCDEFG'   # 注: 不支持汉字
    ciphertext = Aes().encrypt_oracle(str_data)
    plaintext = Aes().decrypt_oralce(ciphertext)

    print("解密结果为: {}".format(plaintext))
    print("密文是: {}\n".format(ciphertext.replace('\n', "")))
