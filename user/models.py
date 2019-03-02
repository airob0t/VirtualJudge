from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
'''一定要继承 AbstractUser，而不是继承 auth.User。尽管 auth.User 继承自 AbstractUser 且并没有对其进行任何额外拓展，
但 AbstractUser 是一个抽象类，而 auth.User 不是。如果你继承了 auth.User 类，这会变成多表继承，在目前的情况下这种继承方式是不被推荐的。
关于 Django 的抽象模型类和多表继承，请查阅 Django 的官方文档 模型继承'''
class User(AbstractUser):
    nickname = models.CharField(max_length=254, blank=True)
    school = models.CharField('学校', max_length=254, null=True)
    solved = models.PositiveIntegerField('解决数', default=0)
    attempted = models.PositiveIntegerField('尝试数', default=0)

    class Meta(AbstractUser.Meta):
        pass


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=True)
#
#     nickname = models.CharField(max_length=254, blank=True)
#     school = models.CharField('学校', max_length=254)
#     solved = models.PositiveIntegerField('解决数', default=0)
#     attempted = models.PositiveIntegerField('尝试数', default=0)
#
#     def __str__(self):
#         return '<UserProfile %s>' % self.user.username