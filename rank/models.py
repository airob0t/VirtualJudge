from django.db import models

# Create your models here.
from contest.models import Contest
from problem.models import Problem
from user.models import User


# 竞赛成绩
class ContestRank(models.Model):
    contest = models.ForeignKey(Contest, verbose_name='比赛', on_delete=False)
    user = models.ForeignKey(User, verbose_name='参赛者', on_delete=False)
    ac = models.PositiveSmallIntegerField('解题数', default=0)
    acproblems = models.ManyToManyField(Problem, verbose_name='已通过题目')
    seconds = models.FloatField('用时', default=0)

    def __str__(self):
        return self.contest.name