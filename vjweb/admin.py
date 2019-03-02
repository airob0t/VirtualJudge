from django.contrib import admin
from vjweb.models import News, OJAccount, OJLanguage
from user.models import User
from problem.models import Problem
from contest.models import Contest
from submission.models import Submission
# Register your models here.

admin.site.site_header = 'VirtualJudge管理系统'
admin.site.site_title = 'VirtualJudge'
# admin.site.register(User)
# admin.site.register(Problem)
# admin.site.register(Contest)
# admin.site.register(Submission)
# admin.site.register(News)
# admin.site.register(OJAccount)
# admin.site.register(OJLanguage)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email', 'date_joined', 'is_active', ]
    list_editable = ['is_active', ]
    search_fields = ('username','email')
    date_hierarchy = 'date_joined'

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'time_limit', 'memory_limit', 'update_time', 'remote_oj',]
    list_filter = ['update_time', 'remote_oj',]
    search_fields = ['title', 'remote_id',]
    date_hierarchy = 'update_time'

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager', 'join_password', 'start_time', 'end_time', 'is_public',]
    list_editable = ['is_public',]
    list_filter = ['manager', 'start_time', 'end_time']
    search_fields = ['name', 'manager',]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['remote_run_id', 'user', 'remote_run_id',  'judge_result', 'retry_count', ]
    search_fields = ['user', ]
    list_filter = ['submit_time', ]
    date_hierarchy = 'submit_time'

    def remote_oj(self, obj):
        return obj.problem.remote_oj

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'release_time', ]
    list_filter = ['author', 'release_time', ]
    search_fields = ['title', 'content', ]
    date_hierarchy = 'release_time'

@admin.register(OJAccount)
class OJAccountAdmin(admin.ModelAdmin):
    list_display = ['oj', 'username', 'password', 'status', ]
    list_editable = ['username', 'password', 'status', ]
    list_filter = ['oj',]
    search_fields = ['username',]

@admin.register(OJLanguage)
class OJLanguage(admin.ModelAdmin):
    list_display = ['oj', 'language_name', 'language_string']
    search_fields = ['oj' ,'language_name', 'language_string']
    list_filter = ['oj', 'language_name']