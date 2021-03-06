# Generated by Django 2.0.1 on 2018-04-18 06:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=254, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('release_time', models.DateTimeField(auto_now=True, verbose_name='发布时间')),
                ('author', models.ForeignKey(on_delete=False, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '公告',
                'verbose_name_plural': '公告',
            },
        ),
        migrations.CreateModel(
            name='OJ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, verbose_name='OJ')),
                ('status', models.BooleanField(default=True, verbose_name='连通性')),
            ],
        ),
        migrations.CreateModel(
            name='OJAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oj', models.CharField(max_length=254, verbose_name='OJ')),
                ('username', models.CharField(max_length=254, verbose_name='用户名')),
                ('password', models.CharField(max_length=254, verbose_name='密码')),
                ('status', models.BooleanField(default=True, verbose_name='可用')),
            ],
            options={
                'verbose_name': '爬虫账号',
                'verbose_name_plural': '爬虫账号',
            },
        ),
        migrations.CreateModel(
            name='OJLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oj', models.CharField(max_length=254, verbose_name='OJ')),
                ('language_name', models.CharField(max_length=254, verbose_name='语言')),
                ('language_string', models.CharField(max_length=254, verbose_name='语言识别符')),
            ],
            options={
                'verbose_name': '编程语言',
                'verbose_name_plural': '编程语言',
            },
        ),
    ]
