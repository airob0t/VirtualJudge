from django.test import TestCase, Client
from problem.models import Problem
from bs4 import BeautifulSoup

# 题目单元测试
class ProblemTest(TestCase):
    def setUp(self):
        self.problem = Problem.objects.create(
            remote_id='1000',
            remote_oj='testoj',
            remote_url='localhost',
            title='测试题目',
            description='题目描述',
            input_description = '输入描述',
            output_description = '输出描述',
            in_sample = '输入样例',
            out_sample = '输出样咧',
            time_limit = '12',
            memory_limit = '64',
        )
        self.client = Client()

    def test_problem_list(self):
        response = self.client.get('/problem/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'lxml')
        trs = soup.find('table').find_all('tr')
        self.assertIn(str(self.problem.id), [tr.find('th').string for tr in trs])


    def test_problem_detail(self):
        response = self.client.get('/problem/{id}'.format(id=self.problem.id))
        self.assertEqual(response.status_code, 200)

    def test_problem_status(self):
        response = self.client.get('/problem/{id}/status'.format(id=self.problem.id))
        self.assertEqual(response.status_code, 200)
