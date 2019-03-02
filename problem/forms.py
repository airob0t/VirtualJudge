from django_select2.forms import *
from submission.models import Submission
from vjweb.models import *
from vjweb.tasks import submit_task

# 代码提交表单
class SourceSubmitForm(forms.ModelForm):
    language = forms.ChoiceField(
        label='语言',
        widget=forms.Select(attrs={'class': 'form-control'}),
        # choices= [ (lang.language_name, lang.language_string) for lang in OJLanguage.objects.all() ]
    )

    source = forms.CharField(
        label='源码',
        min_length=50,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'At least 50 characters'}),
    )

    public = forms.ChoiceField(
        required=False,
        label='公开代码',
        choices=(('False', 'No'), ('True', 'Yes')),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def save(self, commit=True):
        res = super(SourceSubmitForm, self).save(commit=True)
        submit_task.delay(res.id)
        return res

    def __init__(self, *args, **kwargs):
        super(SourceSubmitForm, self).__init__( *args, **kwargs)
        self.fields['language'].choices = OJLanguage.objects.values_list('language_name', 'language_string')

    def set_choices(self, OJ):
        langs = OJLanguage.objects.filter(oj=OJ)
        self.fields['language'].choices = langs.values_list('language_name', 'language_string')

    class Meta:
        model = Submission
        fields = ('language', 'public', 'source')
