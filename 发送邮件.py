#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
发送邮件
注: 需安装yagmail包
pip3 install yagmail
"""
import yagmail as yagmail


class SendAll(object):
    """邮件发送模块"""
    def __init__(self, user, pwd, who, title, content, *what):
        """
        :param user:        用户名
        :param pwd:         密码
        :param who:         发给谁
        :param title:       邮件标题
        :param content:     邮件文本内容
        :param what:        邮件附件
        """
        self.user = user
        self.pwd = pwd
        self.to_who = who
        self.send_what = [i for i in what]
        self.title = title
        self.content = content

    def login_email(self):
        """
        :return:        返回登录邮箱对象
        """
        try:
            yag_server = yagmail.SMTP(user=self.user, password=self.pwd, host="smtp.exmail.qq.com")
        except Exception as e:
            raise Exception('正在执行<发送图片邮件><获取邮件对象>操作失败!' + str(e))
        return yag_server

    def send_action(self):
        """
        发送邮件
        """
        yag_server = self.login_email()
        email_title = self.title
        email_content = self.content
        email_attachments = self.send_what  # 附件列表
        try:
            yag_server.send(self.to_who, email_title, email_content, email_attachments)
            yag_server.close()
        except Exception as e:
            raise Exception('<邮件发送模块>操作失败, 邮件标题: {}'.format(email_title))


