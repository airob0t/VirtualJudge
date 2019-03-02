"""VirtualJudge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django_select2
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView
# from django.contrib.auth import urls as auth_urls
from django.urls import path, include
from vjweb.views import *
from api.views import *
from contest.views import *
from problem.views import *
from rank.views import *
from submission.views import *
from user.views import *




urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=r'static/img/favicon.ico')),
    path('', HomeView.as_view(), name='home'),
    url(r'^select2/', include('django_select2.urls')),
    path('news/<int:news_id>', NewsView.as_view(), name='news'),
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('problem/', ProblemListView.as_view(), name='problemlist'),
    path('problem/<int:problem_id>', ProblemDetailView.as_view(), name='problemdetail'),
    path('problem/<int:problem_id>/submit', ProblemSubmitView.as_view(), name='submit'),
    path('problem/<int:problem_id>/status', ProblemStatusView.as_view(), name='problemstatus'),
    path('problem/<int:problem_id>/submit/<int:contest_id>', ProblemSubmitView.as_view(), name='contestsubmit'),
    path('contest/', ContestListView.as_view(), name='contest'),
    path('contest/<int:contest_id>', ContestDetailView.as_view(), name='contestdetail'),
    path('contest/<int:contest_id>/join', ContestJoinView.as_view(), name='contestjoin'),
    path('contest/<int:contest_id>/change', ContestChangeView.as_view(), name='contestchange'),
    path('contest/<int:contest_id>/delete', ContestDeleteView.as_view(), name='contestdelete'),
    path('contest/<int:contest_id>/status', ContestStatusView.as_view(), name='conteststatus'),
    path('contest/<int:contest_id>/rank', ContestRankView.as_view(), name='contestrank'),
    path('contest/create', ContestCreateView.as_view(), name='contestcreate'),
    path('contest/leave', ContestLeaveView.as_view(), name='contestleave'),
    path('status/', StatusView.as_view(), name='status'),
    path('submission/<int:submission_id>', SubmissionView.as_view(), name='submission'),
    path('rank/', RankView.as_view(), name='rank'),
    path('about/', AboutView.as_view(), name='about'),
    path('profile/<int:user_id>', UserProfileView.as_view(), name='userprofile'),
    path('profile/changdone', UserProfileChangeDoneView.as_view(), name='userprofilechangedone'),
    path('api/updatel', updatel),
    path('api/crawl', crawl),

    # url(r'app/',include(router.urls)),
    path('app/news/', NewsListApi.as_view()),
    path('app/news/<int:pk>', NewsDetailApi.as_view()),
    path('app/problem/', ProblemsListApi.as_view()),
    path('app/problem/<int:pk>',ProblemDetailApi.as_view()),
    path('app/submission/', SubmissionListApi.as_view()),
    path('app/submission/<int:pk>', SubmissionDetailApi.as_view()),
    path('app/contest/', ContestListApi.as_view()),
    path('app/contest/<int:pk>', ContestDetailApi.as_view()),
    path('app/login/', UserLoginApi.as_view(), name='applogin'),
    path('app/logout/', LogoutApi.as_view(), name = 'applogout'),
]
