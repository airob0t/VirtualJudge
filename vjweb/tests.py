from django.test import TestCase, Client
from vjweb.models import News
from user.models import User
from bs4 import BeautifulSoup

# Create your tests here.

class HomeTest(TestCase):
    def setUp(self):
        super(HomeTest, self).setUp()
        self.client = Client()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass


class NewsTest(TestCase):
    def setUp(self):
        super(NewsTest, self).setUp()
        self.client = Client()
        user = User.objects.create_user(username='newstestuser', email='newstestuser@vjudge.top', password='testpassword')
        self.news = News.objects.create(title='标题', content='内容内容内容', author_id=user.id)

    def test_news_list(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'lxml')
        trs = soup.find('table').find_all('tr')
        self.assertIn(str(self.news.id), [ tr.find('th').string for tr in trs ])

    def test_news_detail(self):
        response = self.client.get('/news/{0}'.format(self.news.id))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass


class EmailTest(TestCase):
    pass