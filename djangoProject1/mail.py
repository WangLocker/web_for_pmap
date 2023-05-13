import random

from django.core.mail import send_mail

from djangoProject1 import models


def send_sms_code(to_email):
    """
    发送邮箱验证码
    :param to_mail: 发到这个邮箱
    :return: 成功：0 失败 -1
    """
    # 生成邮箱验证码
    sms_code = '%06d' % random.randint(0, 999999)
    EMAIL_FROM = "m13035308201@163.com"  # 邮箱来自
    email_title = '邮箱动态码登录'
    email_body = "感谢您使用PatenMap，您的邮箱验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(sms_code)
    print(email_body)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [to_email])
    print(send_status)
    return send_status, sms_code

def send_sms_pwd(user):
    id=user.name
    pwd=user.password
    to_email=user.email
    EMAIL_FROM = "m13035308201@163.com"  # 邮箱来自
    email_title = '账号密码找回'
    email_body = "感谢您使用PatenMap，您的用户名为：{0},密码为：{1} 该验证码有效时间为两分钟，请及时进行验证。".format(id,pwd)
    print(email_body)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [to_email])
    print(send_status)
    return send_status
