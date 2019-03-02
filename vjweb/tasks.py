from celery import shared_task, Task

from vjweb.dispatcher import SpiderDispatcher, SubmissionException


class SubmissionTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('on_failure execute')

# 提交任务
@shared_task(bind=True, base=SubmissionTask)
def submit_task(self, submission_id):
    try:
        SpiderDispatcher(submission_id).submit()
    except SubmissionException as e:
        self.retry(exc=e, max_retries=5, countdown=15)