#-*- coding: utf-8 -*-
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models
import urllib
import re
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import psycopg2

class Plan(models.Model):
    _name = 'jm.fetch.plan'

    f1 = fields.Char(u'测试')
    website = fields.Char(u'网站')
    website_comp = fields.Text(u'代码片段')

    def fun(self, cr, uid, *args, **kwargs):
        cr.execute("select website from jm_fetch_plan")
        web_list = cr.fetchall()
        my_sender = 'cooko_fhh@163.com'  # 发件人邮箱账号，为了后面易于维护，所以写成了变量
        my_user = '1207619171@qq.com'  # 收件人邮箱账号，为了后面易于维护，所以写成了变量
        err_list = []
        for web in web_list:
            status = urllib.urlopen(web[0]).code
            if (status != 200):
                err_list.append('网站:'+web[0]+'  错误代码:'+str(status)+'\n')
        if (len(err_list) != 0):
            msg_text = ''
            for err in err_list:
                msg_text += err
            msg = MIMEText(msg_text, 'plain', 'utf-8')
            msg['From'] = formataddr(["CooKo", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["收件人邮箱昵称", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = "官网访问异常代码"  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP("smtp.163.com", 25)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, "ck107326")  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 这句是关闭连接的意思
            print 'ok'

    def local_file(self, cr, uid, *args, **kwargs):
        f = open("C:/Users/CK/Desktop/news.txt",'a+')
        context = f.read()
        print context
        f.close()

        conn = psycopg2.connect(database="sys", user="postgres", password="postgres", host="127.0.0.1",
                                port="65432")
        cur = conn.cursor()

        cur.execute("select idcard from jm_student where id=1")
        info = cur.fetchall()

        print info[0][0]








