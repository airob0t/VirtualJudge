from django.db import models

# Create your models here.
from problem.models import Problem
from user.models import User


# 比赛信息
class Contest(models.Model):
    name = models.CharField('比赛名称', max_length=50)
    description = models.TextField('比赛简介')
    manager = models.ForeignKey(User, verbose_name='组织者', on_delete=False)
    join_password = models.CharField('比赛口令', max_length=50, blank=True, default='')
    problems = models.ManyToManyField(Problem, verbose_name='比赛题目')
    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('结束时间')
    is_public = models.BooleanField('比赛公开')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '比赛'
        verbose_name_plural = '比赛'