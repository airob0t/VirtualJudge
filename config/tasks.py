from celery import shared_task, Task
from django.db.models import F

from VirtualJudgeSpider import config
from VirtualJudgeSpider import control
from vjweb.models import OJLanguage, OJAccount
from problem.models import Problem

# 爬取异常
class CrawlException(Exception):
    def __init__(self, err='Crawl Error'):
        Exception.__init__(self, err)

class CrawlTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('on_failure execute')

# 保存爬取来的题目
def SaveProblem(OJ, remote_prob):
    if remote_prob:
        update_values = dict(
            # remote_oj=OJ,
            remote_url=remote_prob.remote_url,
            # request_status=
            # retry_count=
            title=remote_prob.title,
            description=remote_prob.description,
            input_description=remote_prob.input,
            output_description=remote_prob.output,
            in_sample='',
            out_sample='',
            hint=remote_prob.hint,
            time_limit=remote_prob.time_limit,
            memory_limit=remote_prob.memory_limit,
            source=remote_prob.source,
            special_judge=remote_prob.special_judge,
            sample=remote_prob.sample
        )
        prob, created = Problem.objects.update_or_create(remote_oj=OJ , remote_id=remote_prob.remote_id, defaults=update_values)
    else:
        pass


# 更新OJ语言
@shared_task
def update_OJ_Language():
    OJLanguage.objects.all().delete()
    for oj in control.Controller.get_supports():
        account = OJAccount.objects.filter(oj=oj, status=True)
        if len(account) > 0:
            user = config.Account(account[0].username, account[0].password)
            langs = control.Controller.find_language(oj, account=user)
            print('language',langs)
            if langs:
                OJLangs = []
                for name,lang_string in langs.items():
                    OJLangs.append(OJLanguage(language_name=name, language_string=lang_string, oj=oj))
                OJLanguage.objects.bulk_create(OJLangs)


# 爬取一个题目
@shared_task(bind=True, base=CrawlTask)
def CrawlOneProb(self, OJ, problem_id):
    try:
        remote_prob = control.Controller.get_problem(OJ, problem_id)
        if remote_prob:
            SaveProblem(OJ, remote_prob)
    except CrawlException as e:
        self.retry(exc=e, max_retries=5, countdown=15)


# 爬取所有题目
@shared_task
def CrawlAllProb(OJ):
    control.OJBuilder.build_oj(OJ)
    for probid in control.Controller.get_next_problem_id(OJ):
        CrawlOneProb.delay(OJ, probid)


# 爬取所有题目
@shared_task
def CrawlAllOJAllProb():
    # CrawlAllProb.delay('HDU')
    # CrawlAllProb.delay('POJ')
    for OJ in control.Controller.get_supports():
        CrawlAllProb.delay(OJ)

