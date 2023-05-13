from django.db import models


class User(models.Model):
    '''用户表'''

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    cv = models.CharField(max_length=512)
    c_time = models.DateTimeField(auto_now_add=True)
    region = models.CharField(max_length=128,default='未设置')
    profile = models.CharField(max_length=512,default='无个人简介')
    nick_name = models.CharField(max_length=128,default ='未设置')



    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

class Image(models.Model):
    name = models.CharField(max_length=128)
    image = models.FileField(upload_to='static/pic',default ='未设置')  # 该函数需要安装第三方包pillow