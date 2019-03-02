from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, \
    PasswordResetForm, SetPasswordForm
from django_select2.forms import *
from vjweb.models import *

# 注册表单
class RegisterForm(UserCreationForm):
    from django import forms
    from django.contrib.auth import password_validation
    from django.contrib.auth.forms import UsernameField

    username = UsernameField(
        label='用户名',
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Username'}),
    )

    email = forms.EmailField(
        label='电子邮箱',
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    password1 = forms.CharField(
        label='密码',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='密码确认',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter the same password as before, for verification.'}),
        strip=False,
        help_text='为了校验，请输入与上面相同的密码。',
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

# 用户信息表单
class UserProfileForm(forms.ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname'}),
    )

    school = forms.CharField(
        label='学校',
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School'}),
    )

    def __init__(self, *args, **kwargs):
        self.nickname = forms.CharField(
            label='昵称',
            max_length=254,
            widget=forms.TextInput(attrs={'class': 'form-control', 'value': ''}),
        )

        super(UserProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('nickname', 'school')

# 登录表单
class AuthForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Username'}),
    )
    password = forms.CharField(
        label='密码',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )

# 修改密码表单
class PwdChangeForm(PasswordChangeForm):
    from django import forms

    old_password = forms.CharField(
        label='旧密码',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old password'}),
    )

    new_password1 = forms.CharField(
        label='新密码',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'}),
    )

    new_password2 = forms.CharField(
        label='新密码确认',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter the same password as before, for verification.'}),
    )

# 密码重置表单
class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='电子邮箱',
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )


# 初始密码表单
class SetPwdForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='新密码',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'}),
    )

    new_password2 = forms.CharField(
        label='新密码确认',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter the same password as before, for verification.'}),
    )