from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView

from VirtualJudge.settings import NEWS_PER_PAGE



# Create your views here.
from vjweb.models import News


def updatel(request):
    from config import tasks
    tasks.update_OJ_Language.delay()
    return HttpResponse('update')

def crawl(request):
    from config import tasks
    tasks.CrawlAllOJAllProb.delay()
    return HttpResponse('Run')

class AboutView(TemplateView):
    template_name = 'about.html'


# 主页视图
class HomeView(ListView):
    model = News
    template_name = 'home.html'
    context_object_name = 'news_list'
    paginate_by = NEWS_PER_PAGE
    ordering = ['-release_time']


# 公告视图
class NewsView(DetailView):
    model = News
    template_name = 'news.html'
    pk_url_kwarg = 'news_id'



