from django_select2.forms import *

from contest.models import Contest
from problem.models import Problem


# 创建/修改比赛的表单
class ContestForm(forms.ModelForm):
    name = forms.CharField(
        label='比赛名称',
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contestname'}),
    )

    description = forms.CharField(
        label='比赛介绍',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    join_password = forms.CharField(
        label='比赛口令',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '比赛设为非公开口令才会生效'}),
    )

    start_time = forms.DateTimeField(
        label='开始时间',
        widget=forms.DateTimeInput(attrs={'class': 'form_datetime form-control'}),
        help_text='如无特殊情况，开始时间应当早于结束时间'
    )

    end_time = forms.DateTimeField(
        label='结束时间',
        widget=forms.DateTimeInput(attrs={'class': 'form_datetime form-control'}),
        help_text='如无特殊情况，开始时间应当早于结束时间'
    )

    problems = forms.ModelMultipleChoiceField(
        label='题目',
        queryset=Problem.objects.all(),
        widget=ModelSelect2MultipleWidget(model=Problem, search_fields=['title__icontains'], attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Contest
        fields = ('name', 'description', 'join_password', 'problems', 'start_time', 'end_time', 'is_public')
        # widgets = {
        #     'problems': forms.SelectMultiple(attrs={'class': 'form-control'})
        # }