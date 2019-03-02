from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, TemplateView

# from user.models import User, UserProfile
from user.forms import RegisterForm, AuthForm, PwdChangeForm, PwdResetForm, SetPwdForm, UserProfileForm
from user.models import User
from vjweb.forms import *
from django.contrib.auth import views as auth_views

# 注册视图
class RegisterView(CreateView):
    model = User
    pk_url_kwarg = 'next'
    form_class = RegisterForm
    success_url = reverse_lazy('home')
    template_name = 'registration/register.html'

    def dispatch(self, request, *args, **kwargs):
        # redirect_to = request.POST.get('next', False)
        self.success_url = reverse_lazy('home')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

# 登录视图
class LoginView(auth_views.LoginView):
    form_class = AuthForm

# 注销视图
class LogoutView(auth_views.LogoutView):
    pass

# 更改密码视图
class PasswordChangeView(auth_views.PasswordChangeView):
    form_class = PwdChangeForm

# 更改密码完成视图
class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    pass

# 密码重置视图
class PasswordResetView(auth_views.PasswordResetView):
    form_class = PwdResetForm

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
            'domain_override': 'vjudge.top', #覆写domain
        }
        form.save(**opts)
        return HttpResponseRedirect(self.success_url)

# 密码重置确认视图
class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = SetPwdForm

# 密码重置完成视图
class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    pass

# 密码重成功视图
class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    pass


# 个人信息视图
class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'registration/profile_change.html'
    context_object_name = 'userprofile'
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('userprofilechangedone')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfileView, self).dispatch(request, *args, **kwargs)


# 个人信息修改成功视图
class UserProfileChangeDoneView(TemplateView):
    template_name = 'registration/profile_change_done.html'
