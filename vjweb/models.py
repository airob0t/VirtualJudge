# from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from user.models import User

# 公告
class News(models.Model):
    title = models.CharField('标题', max_length=254)
    content = models.TextField('内容')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=False)
    release_time = models.DateTimeField('发布时间', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'

# 爬虫账号
class OJAccount(models.Model):
    oj = models.CharField('OJ', max_length=254)
    username = models.CharField('用户名', max_length=254)
    password = models.CharField('密码', max_length=254)
    status = models.BooleanField('可用', default=True)

    def __str__(self):
        return self.oj+','+self.username

    class Meta:
        verbose_name = '爬虫账号'
        verbose_name_plural = '爬虫账号'

# OJ语言
class OJLanguage(models.Model):
    oj = models.CharField('OJ', max_length=254)
    language_name = models.CharField('语言', max_length=254)
    language_string = models.CharField('语言识别符', max_length=254)

    def __str__(self):
        return self.oj+','+self.language_name

    class Meta:
        verbose_name = '编程语言'
        verbose_name_plural = '编程语言'

# # OJ
# class OJ(models.Model):
#     name = models.CharField('OJ', max_length=254)
#     status = models.BooleanField('连通性', default=True)
#     # others = models.CharField('其它', max_length=254)
#
#     def __str__(self):
#         return self.name