import time

from VirtualJudgeSpider.config import Account, ACName
from VirtualJudgeSpider.control import Controller
from django.db import transaction

from rank.models import ContestRank
from utils.definition import JudgeRequest
from vjweb.models import OJAccount
from submission.models import  Submission
# from user.models import UserProfile



class SubmissionException(Exception):
    def __init__(self, err='Submission Error'):
        Exception.__init__(self, err)


class SpiderDispatcher(object):
    def __init__(self, submission_id):
        self.submission = Submission.objects.get(id=submission_id)
        self.remote_account = None

    # 选择账号
    @staticmethod
    def choose_account(remote_oj):
        with transaction.atomic():
            remote_accounts = OJAccount.objects.filter(oj=remote_oj, status=True)
            # print('accounts', remote_accounts)
            if remote_accounts:
                remote_account = remote_accounts[0]
                remote_account.status = False
                remote_account.save()
                return remote_account
        return None

    # 释放账号
    @staticmethod
    def release_account(remote_account_id):
        with transaction.atomic():
            remote_account = OJAccount.objects.get(id=remote_account_id)
            remote_account.status = True
            remote_account.save()

    # 等待评测
    def waiting_for_judge(self):
        for i in range(10):
            result = Controller.get_result_by_rid(self.submission.problem.remote_oj, self.submission.remote_run_id)
            if Controller.is_waiting_for_judge(self.submission.problem.remote_oj, result.verdict):
                self.submission.status = JudgeRequest.status['JUDGING']
                # self.submission.retry_count = self.submission.retry_count + 1
                self.submission.save()
                time.sleep(1)
            else:
                self.submission.judge_result = result.verdict
                self.submission.execute_memory = result.execute_memory
                self.submission.execute_time = result.execute_time
                self.submission.status = JudgeRequest.status['SUCCESS']
                self.submission.save()
                return True
        return False

    def retry(self):
        self.submission.retry_count = self.submission.retry_count + 1
        self.submission.save()

    # 更新成绩信息
    def update_statistic(self):
        # update statistic info
        with transaction.atomic():
            self.submission.problem.submit += 1
            self.submission.user.attempted += 1
            # user, created = UserProfile.objects.get_or_create(user=self.submission.user)
            # if created:
            #     user.attempted += 1
            # else:
            #     # 创建个人信息失败
            #     pass

            # print(self.submission.judge_result, ACName.names[self.submission.problem.remote_oj])
            # print(type(self.submission.judge_result), type(ACName.names[self.submission.problem.remote_oj]))
            if self.submission.judge_result == ACName.names[self.submission.problem.remote_oj]:
                self.submission.problem.accepted += 1
                # user.solved += 1
                self.submission.user.solved += 1
            self.submission.problem.save()
            # user.save()
            self.submission.user.save()
            # print(self.submission.contest)
            if self.submission.contest:
                rank, created = ContestRank.objects.get_or_create(contest=self.submission.contest,
                                                                  user=self.submission.user)
                if self.submission.judge_result == ACName.names[
                    self.submission.problem.remote_oj] and self.submission.problem not in rank.acproblems.all():
                    wrong_cnt = Submission.objects.filter(
                        contest=self.submission.contest,
                        user=self.submission.user,
                        problem=self.submission.problem).exclude(
                        judge_result=ACName.names[self.submission.problem.remote_oj]).count()
                    rank.ac += 1
                    rank.seconds += self.submission.submit_time.timestamp() - self.submission.contest.start_time.timestamp()
                    rank.seconds += wrong_cnt * 20 * 60
                rank.save()

    # 提交
    def submit(self):
        if self.submission.retry_count > 10:
            return
        if self.submission.status == JudgeRequest.status['PENDING'] or \
                self.submission.status == JudgeRequest.status['SEND_FOR_JUDGE_ERROR']:
            account = self.choose_account(self.submission.problem.remote_oj)
            # print('account', account, self.submission.problem.remote_oj)
            if not account:
                self.retry()
                raise SubmissionException
            success_submit = Controller.submit_code(self.submission.problem.remote_oj,
                                                    Account(username=account.username, password=account.password),
                                                    self.submission.source,
                                                    self.submission.language,
                                                    self.submission.problem.remote_id)
            # print('success_submit', success_submit)
            if success_submit:
                result = Controller.get_result(self.submission.problem.remote_oj,
                                               Account(username=account.username, password=account.password),
                                               self.submission.problem.remote_id)
                # print('result', result)
                # 结果返回有误
                if not result:
                    if self.submission.status == JudgeRequest.status['SEND_FOR_JUDGE_ERROR']:
                        self.submission.status = JudgeRequest.status['RETRY']
                    else:
                        self.submission.status = JudgeRequest.status['SEND_FOR_JUDGE_ERROR']
                    self.release_account(account.id)
                    self.retry()
                    raise Submission
                self.submission.remote_run_id = result.origin_run_id
                self.submission.judge_result = result.verdict
                self.submission.execute_memory = result.execute_memory
                self.submission.execute_time = result.execute_time
                self.submission.save()
                if self.waiting_for_judge():
                    print('submit_success')
                    self.update_statistic()
                else:
                    self.submission.status = JudgeRequest.status['RETRY']
                    self.release_account(account.id)
                    self.retry()
                    raise SubmissionException
            else:
                # 提交失败
                if self.submission.status == JudgeRequest.status['SEND_FOR_JUDGE_ERROR']:
                    self.submission.status = JudgeRequest.status['RETRY']
                else:
                    self.submission.status = JudgeRequest.status['SEND_FOR_JUDGE_ERROR']
                    self.retry()
                self.release_account(account.id)
                raise SubmissionException
            self.release_account(account.id)
