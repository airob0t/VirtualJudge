from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from VirtualJudge.settings import USERS_PER_PAGE
from contest.models import Contest
from rank.models import ContestRank
from user.models import User

# 积分视图
class RankView(ListView):
    model = User
    template_name = 'rank.html'
    context_object_name = 'user_list'
    paginate_by = USERS_PER_PAGE
    # ordering = ['-solved']

    # 预处理是否参加竞赛
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('contest', None):
            return HttpResponseRedirect(reverse('contestrank', kwargs={'contest_id': request.session.get('contest', None)}))
        return super(RankView, self).dispatch(request, *args, **kwargs)

    # 过滤数据
    def get_queryset(self):
        rank_id = self.request.GET.get('id', None)
        username = self.request.GET.get('username', None)
        nickname = self.request.GET.get('nickname', None)
        school = self.request.GET.get('school', None)
        queryset = self.model.objects.order_by('-solved').all()
        if rank_id:
            queryset = queryset.filter(id=rank_id)
        if username:
            queryset = queryset.filter(user__username__icontains=username)
        if nickname:
            queryset = queryset.filter(nickname__icontains=nickname)
        if school:
            queryset = queryset.filter(school__icontains=school)
        return queryset


# 比赛排名视图
class ContestRankView(ListView):
    model = ContestRank
    template_name = 'contest/contest_rank.html'
    context_object_name = 'contestrank_list'
    paginate_by = USERS_PER_PAGE
    pk_url_kwarg = 'contest_id'
    # ordering = ['-ac']

    # 处理参加竞赛的逻辑
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        contest = Contest.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        if not contest.is_public and request.session.get('joinpassword', None) != contest.join_password:
            return HttpResponseRedirect(reverse('contestjoin', kwargs={'contest_id': contest.id}))
        self.queryset = ContestRank.objects.filter(contest=kwargs[self.pk_url_kwarg]).prefetch_related('acproblems')
        return super(ContestRankView, self).dispatch(request, *args, **kwargs)

    # 过滤数据
    def get_queryset(self):
        rank_id = self.request.GET.get('id', None)
        username = self.request.GET.get('username', None)
        nickname = self.request.GET.get('nickname', None)
        school = self.request.GET.get('school', None)
        queryset = self.queryset.order_by('-ac')
        if rank_id:
            queryset = queryset.filter(id=rank_id)
        if username:
            queryset = queryset.filter(user__username__icontains=username)
        if nickname:
            queryset = queryset.filter(nickname__icontains=nickname)
        if school:
            queryset = queryset.filter(school__icontains=school)
        return queryset
