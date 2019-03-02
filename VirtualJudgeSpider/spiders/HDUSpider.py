import re

import requests
from bs4 import BeautifulSoup

from VirtualJudgeSpider import config
from VirtualJudgeSpider.config import Problem, Result
from VirtualJudgeSpider.spiders.BaseSpider import Base


class HDU(Base):
    def __init__(self):
        self.code_type = 'gb18030'
        self.headers = config.custom_headers
        self.cookies = None
        self.request = requests.session()
        self.request.headers.update(config.custom_headers)

    @staticmethod
    def home_page_url(self):
        url = 'http://acm.hdu.edu.cn/'
        return url

    def check_login_status(self):
        url = 'http://acm.hdu.edu.cn/'
        try:
            website_data = self.request.get(url)
            self.cookies = website_data.cookies
            if re.search(r'userloginex\.php\?action=logout', website_data.text) is not None:
                return True
            return False
        except:
            return False

    def login_website(self, *args, **kwargs):
        if self.check_login_status():
            return True
        login_page_url = 'http://acm.hdu.edu.cn/'
        login_link_url = 'http://acm.hdu.edu.cn/userloginex.php?action=login&cid=0&notice=0'

        post_data = {'username': kwargs['account'].get_username(), 'userpass': kwargs['account'].get_password()}
        try:
            req1 = self.request.get(login_page_url)
            self.cookies = req1.cookies
            req2 = self.request.post(url=login_link_url, data=post_data)
            self.cookies = req2.cookies
            if self.check_login_status():
                return True
            return False
        except:
            return False

    def get_problem(self, *args, **kwargs):
        url = 'http://acm.hdu.edu.cn/showproblem.php?pid=' + str(kwargs['pid'])
        problem = Problem()
        try:
            website_data = self.request.get(url)
            self.cookies = website_data.cookies
            problem.remote_id = kwargs['pid']
            problem.remote_url = url
            problem.remote_oj = 'HDU'
            problem.title = re.search(r'color:#1A5CC8\'>([\s\S]*?)</h1>', website_data.text).group(1)
            problem.time_limit = re.search(r'(\d* MS)', website_data.text).group(1)
            problem.memory_limit = re.search(r'/(\d* K)', website_data.text).group(1)
            problem.special_judge = re.search(r'color=red>Special Judge</font>', website_data.text) is not None
            problem.description = re.search(r'>Problem Description</div>[\s\S]*?panel_content>([\s\S]*?)</div>',
                                            website_data.text).group(1)
            problem.input = re.search(r'>Input</div>[\s\S]*?panel_content>([\s\S]*?)</div>', website_data.text).group(1)
            problem.output = re.search(r'>Output</div>[\s\S]*?panel_content>([\s\S]*?)</div>', website_data.text).group(
                1)
            match_group = re.search(r'>Sample Input</div>[\s\S]*?panel_content>([\s\S]*?)</div', website_data.text)
            input_data = ''

            if match_group:
                input_data = re.search(r'(<pre><div[\s\S]*?>)?([\s\S]*)', match_group.group(1)).group(2)

            output_data = ''
            match_group = re.search(r'>Sample Output</div>[\s\S]*?panel_content>([\s\S]*?)</div', website_data.text)
            if match_group:
                output_data = re.search(r'(<pre><div[\s\S]*?>)?([\s\S]*)', match_group.group(1)).group(2)
                if re.search('<div', output_data):
                    output_data = re.search(r'([\s\S]*?)<div', output_data).group(1)
            problem.sample = [
                {'input': input_data,
                 'output': output_data}]

            match_group = re.search(r'>Author</div>[\s\S]*?panel_content>([\s\S]*?)</div>', website_data.text)
            if match_group:
                problem.author = match_group.group(1)
            match_group = re.search(r'<i>Hint</i>[\s\S]*?/div>[\s]*([\s\S]+?)</div>', website_data.text)
            if match_group:
                problem.hint = match_group.group(1)
        except:
            return None
        return problem

    def submit_code(self, *args, **kwargs):
        if not self.login_website(*args, **kwargs):
            return False
        try:
            code = kwargs['code']
            language = kwargs['language']
            pid = kwargs['pid']
            url = 'http://acm.hdu.edu.cn/submit.php?action=submit'
            post_data = {'check': '0', 'language': language, 'problemid': pid, 'usercode': code}
            res = self.request.post(url, data=post_data)
            self.cookies = res.cookies
            # print(res.status_code)
            if res.status_code == 200:
                return True
            return False
        except:
            return False

    def find_language(self, *args, **kwargs):
        if not self.login_website(*args, **kwargs):
            return None
        url = 'http://acm.hdu.edu.cn/submit.php'
        languages = {}
        try:
            website_data = self.request.get(url)
            self.cookies = website_data.cookies
            soup = BeautifulSoup(website_data.text, 'lxml')
            options = soup.find('select', attrs={'name': 'language'}).find_all('option')
            for option in options:
                # print(type(option.get('value')), option.get('value'), option.string)
                languages[option.get('value')] = option.string
        finally:
            # print(languages)
            return languages

    def get_result(self, *args, **kwargs):
        account = kwargs.get('account')
        pid = kwargs.get('pid')
        url = 'http://acm.hdu.edu.cn/status.php?first=&pid=' + pid + '&user=' + account.username + '&lang=0&status=0'
        return self.get_result_by_url(url=url)

    def get_result_by_rid(self, rid):
        url = 'http://acm.hdu.edu.cn/status.php?first=' + rid + '&pid=&user=&lang=0&status=0'
        return self.get_result_by_url(url=url)

    def get_result_by_url(self, url):
        result = Result()
        try:
            data = self.request.get(url)
            self.cookies = data.cookies
            soup = BeautifulSoup(data.text, 'lxml')
            line = soup.find('table', attrs={'class': 'table_text'}).find('tr', attrs={'align': 'center'}).find_all(
                'td')
            if line is not None:
                result.origin_run_id = line[0].string
                result.verdict = line[2].string
                result.execute_time = line[4].string
                result.execute_memory = line[5].string
                return result
        except:
            pass
        return result

    def get_class_name(self):
        return str('HDU')

    def is_waiting_for_judge(self, verdict):
        if verdict in ['Queuing', 'Compiling', 'Running']:
            return True
        return False

    def check_status(self):
        url = 'http://acm.hdu.edu.cn/'
        try:
            website_data = requests.get(url)
            self.cookies = website_data.cookies
            if re.search(r'<H1>Welcome to HDU Online Judge System</H1>', website_data.text):
                return True
        except:
            return False

    def get_next_problem_id(self):
        url = 'http://acm.hdu.edu.cn/listproblem.php'
        problemid = None
        req = self.request.get(url)
        soup = BeautifulSoup(req.text, 'lxml')
        tags_p = soup.find('p', attrs={'class': 'footer_link'})
        tags_a = tags_p.find_all('a')
        pages = [tag_a.string for tag_a in tags_a]
        try:
            for page in pages:
                listpage_url = url+'?vol='+str(page)
                listpage = self.request.get(listpage_url)
                soup = BeautifulSoup(listpage.text, 'lxml')
                table = soup.find('table', attrs={'class': 'table_text'})
                probjs = table.find('script').string.strip(';').split(';')
                problems = [ prob[2:-1].split(',') for prob in probjs ]
                for prob in problems:
                    problemid = prob[1]
                    yield problemid
        finally:
            return problemid