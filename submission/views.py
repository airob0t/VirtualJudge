from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from VirtualJudge.settings import SUBMISSIONS_PER_PAGE, PROBLEMS_PER_PAGE
from submission.models import Submission
from vjweb.forms import *

# 提交记录视图
class StatusView(ListView):
    model = Submission
    template_name = 'status.html'
    context_object_name = 'submission_list'
    paginate_by = SUBMISSIONS_PER_PAGE
    ordering = ['-submit_time']

    # 预处理是否参加竞赛
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('contest', None):
            return HttpResponseRedirect(reverse('conteststatus', kwargs={'contest_id': request.session.get('contest', None)}))
        return super(StatusView, self).dispatch(request, *args, **kwargs)

    # 过滤数据
    def get_queryset(self):
        username = self.request.GET.get('username', None)
        probname = self.request.GET.get('probname', None)
        oj = self.request.GET.get('oj', None)
        submission_id = self.request.GET.get('id', None)
        queryset = self.model.objects.order_by('-submit_time').all()
        if submission_id:
            queryset = queryset.filter(id=submission_id)
        if username:
            queryset = queryset.filter(user__username__icontains=username)
        if probname:
            queryset = queryset.filter(problem__title__icontains=probname)
        if oj:
            queryset = queryset.filter(problem__remote_oj__exact=oj)
        return queryset


# 提交记录详细信息视图
class SubmissionView(DetailView):
    model = Submission
    template_name = 'submission/submission.html'
    pk_url_kwarg = 'submission_id'

    # 处理权限
    def dispatch(self, request, *args, **kwargs):
        sub = get_object_or_404(self.model, id=kwargs[self.pk_url_kwarg])
        if (not sub.public or request.session.get('contest', None)) and sub.user != request.user:
            raise Http404('无访问权限')
        return super(SubmissionView, self).dispatch(request, *args, **kwargs)



# 比赛提交记录视图
class ContestStatusView(ListView):
    model = Submission
    template_name = 'status.html'
    context_object_name = 'submission_list'
    paginate_by = PROBLEMS_PER_PAGE
    ordering = ['-submit_time']
    pk_url_kwarg = 'contest_id'

    # 预处理数据
    def dispatch(self, request, *args, **kwargs):
        self.queryset = self.model.objects.filter(contest=kwargs[self.pk_url_kwarg]).order_by('-submit_time')
        return super(ContestStatusView, self).dispatch(request, *args, **kwargs)

    # 过滤数据
    def get_queryset(self):
        username = self.request.GET.get('username', None)
        probname = self.request.GET.get('probname', None)
        oj = self.request.GET.get('oj', None)
        submission_id = self.request.GET.get('id', None)
        queryset = self.queryset
        if submission_id:
            queryset = queryset.filter(id=submission_id)
        if username:
            queryset = queryset.filter(user__username__icontains=username)
        if probname:
            queryset = queryset.filter(problem__title__icontains=probname)
        if oj:
            queryset = queryset.filter(problem__remote_oj__exact=oj)
        return queryset