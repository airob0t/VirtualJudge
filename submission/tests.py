from django.test import TestCase, Client

# Create your tests here.
class StatusTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_status(self):
        response = self.client.get('/status/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass

# ToDo
class SubmissionTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_submission(self):
        pass

    def tearDown(self):
        pass