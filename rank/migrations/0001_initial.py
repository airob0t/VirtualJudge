# Generated by Django 2.0.1 on 2018-04-18 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contest', '0001_initial'),
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContestRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ac', models.PositiveSmallIntegerField(default=0, verbose_name='解题数')),
                ('seconds', models.FloatField(default=0, verbose_name='用时')),
                ('acproblems', models.ManyToManyField(to='problem.Problem', verbose_name='已通过题目')),
                ('contest', models.ForeignKey(on_delete=False, to='contest.Contest', verbose_name='比赛')),
            ],
        ),
    ]
