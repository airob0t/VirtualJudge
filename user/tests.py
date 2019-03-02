from django.test import TestCase, Client
from user.models import User

# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='usertest', email='usertest@vjudge.top', password='testpassword')
        self.client = Client()

    def test_register(self):
        response = self.client.post('/accounts/register/',
                                    {'username': 'registertest', 'email': 'registertest@vjudge.top',
                                     'password1': 'testpassword', 'password2': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.login(username='registertest', password='testpassword'), True)
        response = self.client.get('/profile/{user_id}'.format(user_id=User.objects.get(username='registertest').id))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_user(self):
        self.assertEqual(self.client.login(username='usertest', password='testpassword'), True)
        response = self.client.get('/profile/{user_id}'.format(user_id=self.user.id))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass
