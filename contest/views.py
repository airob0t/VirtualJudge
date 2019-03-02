from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from VirtualJudge.settings import CONTESTS_PER_PAGE
from contest.forms import ContestForm
from contest.models import Contest

# 比赛列表视图
class ContestListView(ListView):
    model = Contest
    template_name = 'contest.html'
    context_object_name = 'contest_list'
    paginate_by = CONTESTS_PER_PAGE
    ordering = ['-start_time']

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('contest', None):
            return HttpResponseRedirect(reverse('contestdetail', kwargs={'contest_id': request.session.get('contest', None)}))
        return super(ContestListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        name = self.request.GET.get('name', None)
        queryset = self.model.objects.order_by('start_time').all()
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


# 比赛详细信息视图
class ContestDetailView(DetailView):
    model = Contest
    template_name = 'contest/contest_detail.html'
    context_object_name = 'contest'
    pk_url_kwarg = 'contest_id'

    def dispatch(self, request, *args, **kwargs):
        contest = Contest.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        if not contest.is_public and request.session.get('joinpassword', '') != contest.join_password:
            return HttpResponseRedirect(reverse('contestjoin', kwargs={'contest_id': contest.id}))
        self.queryset = Contest.objects.filter(pk=self.kwargs[self.pk_url_kwarg]).prefetch_related('problems')
        return super(ContestDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContestDetailView, self).get_context_data(**kwargs)
        if self.request.session.get('contest', None):
            context['contest'] = Contest.objects.get(id=self.request.session.get('contest', None))
        return context


# 比赛创建视图
class ContestCreateView(CreateView):
    model = Contest
    form_class = ContestForm
    template_name = 'contest/contest_create.html'
    success_url = reverse_lazy('contest')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ContestCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super(ContestCreateView, self).form_valid(form)


# 比赛参加视图
class ContestJoinView(DetailView):
    model = Contest
    pk_url_kwarg = 'contest_id'
    template_name = 'contest/contest_joinauth.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.contest = Contest.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        if now() < self.contest.start_time or now() > self.contest.end_time:
            return render(request, 'info.html', {'info': '不在比赛时间内！', 'path': '/contest' })
        return super(ContestJoinView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # contest = Contest.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        if self.contest.is_public:
            if not request.session.get('contest', None):
                request.session['contest'] = self.contest.id
            return HttpResponseRedirect(reverse('contestdetail', kwargs={'contest_id': self.contest.id}))
        return super(ContestJoinView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # contest = Contest.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        if request.POST.get('joinpassword', '') == self.contest.join_password:
            request.session['contest'] = self.contest.id
            request.session['joinpassword'] = self.contest.join_password
            return HttpResponseRedirect(reverse('contestdetail', kwargs={'contest_id': self.contest.id}))
        return render(request, self.template_name, {'info': '比赛口令错误！'})


# 比赛离开视图
class ContestLeaveView(TemplateView):
    template_name = 'contest/contest_leave.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        request.session.pop('contest')
        return super(ContestLeaveView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContestLeaveView, self).get_context_data(**kwargs)
        context['info'] = '你已经离开竞赛'
        return context


# 比赛修改视图
class ContestChangeView(UpdateView):
    model = Contest
    form_class = ContestForm
    template_name = 'contest/contest_change.html'
    context_object_name = 'contest'
    pk_url_kwarg = 'contest_id'
    success_url = reverse_lazy('contest')


# 比赛删除视图
class ContestDeleteView(DeleteView):
    model = Contest
    template_name = 'contest/contest_delete_confirm.html'
    pk_url_kwarg = 'contest_id'
    success_url = reverse_lazy('contest')
