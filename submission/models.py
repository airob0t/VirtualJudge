from django.db import models

# Create your models here.
from contest.models import Contest
from problem.models import Problem
from user.models import User

# 提交记录
class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=False)
    source = models.TextField('源码')
    submit_time = models.DateTimeField('提交时间', auto_now=True)
    contest = models.ForeignKey(Contest, on_delete=False, verbose_name='比赛', null=True)
    problem = models.ForeignKey(Problem, on_delete=False, verbose_name='题目', null=True)
    status = models.IntegerField('状态', default=0)
    public = models.BooleanField('公开代码', default=False)
    language = models.CharField('语言', default='C++', max_length=254)
    remote_run_id = models.CharField('原OJ运行id',max_length=254, null=True)
    judge_result = models.CharField('裁判结果', max_length=254, null=True)
    execute_time = models.CharField('程序运行时间', max_length=254, null=True)
    execute_memory = models.CharField('程序运行内存', max_length=254, null=True)
    compile_info = models.TextField('编译信息', null=True)
    retry_count = models.IntegerField('重试次数', default=0)
    spider_status = models.IntegerField(null=True)

    def __str__(self):
        return self.user.username+', '+self.problem.title

    class Meta:
        verbose_name = '提交记录'
        verbose_name_plural = '提交记录'