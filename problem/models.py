from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.
# 题目信息
class Problem(models.Model):
    # from django.contrib.postgres.fields import JSONField

    remote_oj = models.CharField('原OJ', max_length=254, null=True)
    remote_id = models.CharField('原OJ题目id', max_length=254, null=True)
    remote_url = models.CharField('愿题目地址', max_length=254, null=True)
    request_status = models.IntegerField('请求状态', default=0)
    retry_count = models.IntegerField('重试次数', default=0)

    title = models.CharField('题目名称', max_length=254)
    description = models.TextField('题面')
    input_description = models.TextField('输入描述')
    output_description = models.TextField('输出描述')
    in_sample = models.TextField('输入样例')
    out_sample = models.TextField('输出样咧')
    hint = models.TextField('提示', null=True)
    time_limit = models.CharField('时间限制', max_length=254)
    memory_limit = models.CharField('内存限制', max_length=254)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    accepted = models.PositiveIntegerField('通过数', default=0)
    submit = models.PositiveIntegerField('提交数', default=0)
    source = models.CharField('来源',max_length=254 , default='defaultnull', null=True)
    special_judge = models.BooleanField('SPJ', default=False)
    sample = JSONField('样例', null=True, blank=True)
    #link = "Edit"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = '题目'