from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default=u'')
    image = models.ImageField(max_length=100,upload_to='image/%Y%m', default=u'image/default.png', verbose_name=u'头像')
    gender = models.CharField(max_length=5, choices=(('male', u'男'),('female','女')), default='female', verbose_name=u'性别')
    birday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    address = models.CharField(max_length=100, verbose_name=u'地址', default=u'')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name=u'电话')

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    # def get_unread_nums(self):
    #     from operation.models import UserMessage
    #     return UserMessage.objects.filter(user=self.id, has_read=False).count()

class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.CharField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(max_length=10, choices=(('register',u'注册'),('forget',u'找回密码'),('update', u'修改邮箱')), verbose_name=u'发送类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'邮箱验证'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email

class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image= models.ImageField(max_length=100, upload_to='banner/%Y%m', verbose_name=u'轮播图')
    url = models.URLField(max_length=200, verbose_name=u'访问地址')
    index = models.IntegerField(default=1, verbose_name=u'访问顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
