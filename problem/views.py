from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.generic import ListView, DetailView, CreateView

from VirtualJudge.settings import PROBLEMS_PER_PAGE
from contest.models import Contest
from problem.forms import SourceSubmitForm
from problem.models import Problem
from submission.models import Submission
from utils.definition import JudgeRequest

# 题目列表视图
from vjweb.models import OJLanguage

# 题目列表视图
class ProblemListView(ListView):
    model = Problem
    context_object_name = 'problem_list'
    template_name = 'problem.html'
    paginate_by = PROBLEMS_PER_PAGE
    ordering = ['-update_time']

    # 预处理是否参加竞赛的情况
    def get_context_data(self, **kwargs):
        context = super(ProblemListView, self).get_context_data(**kwargs)
        if self.request.session.get('contest', None):
            context['contest'] = Contest.objects.get(id=self.request.session.get('contest', None))
        return context

    # 根据状态过滤数据
    def get_queryset(self):
        contest = self.request.session.get('contest', None)
        name = self.request.GET.get('name', None)
        pid = self.request.GET.get('id', None)

        queryset = self.model.objects.order_by('-update_time').all()
        if contest:
            queryset = Contest.objects.get(id=contest).problems.all()
        if name:
            queryset = queryset.filter(title__icontains=name)
        if pid:
            queryset = queryset.filter(id=pid)
        return queryset


# 题目详细信息视图
class ProblemDetailView(DetailView):
    model = Problem
    template_name = 'problem/problem_detail.html'
    context_object_name = 'problem'
    pk_url_kwarg = 'problem_id'


# 题目提交视图
class ProblemSubmitView(CreateView):
    model = Submission
    pk_url_kwarg = 'problem_id'
    default_status = JudgeRequest.status['PENDING']
    form_class = SourceSubmitForm
    success_url = reverse_lazy('status')
    template_name = 'problem/problem_submit.html'

    # 要求登录状态
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProblemSubmitView, self).dispatch(request, *args, **kwargs)

    # 预处理是否参加竞赛的情况
    def get_context_data(self, **kwargs):
        context = super(ProblemSubmitView, self).get_context_data(**kwargs)
        contestid = self.request.session.get('contest', None)
        if contestid:
            contest = Contest.objects.get(pk=contestid)
            if now() >= contest.start_time and now()<= contest.end_time:
                # context['incontest'] = contestid
                context['contest'] = contest
            else:
                self.request.session.pop('contest')
        problem = Problem.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        form = SourceSubmitForm()
        form.set_choices(OJ=problem.remote_oj)
        context['form'] = form
        return context

    # 表单合法后的处理
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = self.default_status
        form.instance.problem = Problem.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        if self.request.session.get('contest', None):
            contest = Contest.objects.get(pk=self.request.session.get('contest', None))
            if now() >= contest.start_time and now()<= contest.end_time and form.instance.problem in contest.problems.all():
                form.instance.contest = contest
            elif form.instance.problem not in contest.problems.all():
                # 题目非比赛题目
                pass
            else:
                self.request.session.pop('contest')
        # 改为提交成功后更新记录
        # UserProfile.objects.filter(user=self.request.user.pk).update(attempted=F('attempted')+1)
        # Problem.objects.filter(pk=self.kwargs[self.pk_url_kwarg]).update(submit=F('submit')+1)
        return super(ProblemSubmitView, self).form_valid(form)


# 题目提交记录视图
class ProblemStatusView(ListView):
    model = Submission
    template_name = 'status.html'
    context_object_name = 'submission_list'
    paginate_by = PROBLEMS_PER_PAGE
    ordering = ['-submit_time']
    pk_url_kwarg = 'problem_id'

    # 预处理数据集
    def dispatch(self, request, *args, **kwargs):
        self.queryset = self.model.objects.filter(problem=kwargs[self.pk_url_kwarg])
        return super(ProblemStatusView, self).dispatch(request, *args, **kwargs)

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