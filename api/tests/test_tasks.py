from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.conf import settings

class RateLimitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", email="tester@test.com")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.task_url = "/api/tasks/"
        self.rate_limit = int(settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['user'].split('/')[0])

    def test_rate_limit(self):        
        for _ in range(self.rate_limit):
            response = self.client.get(self.task_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertIn("Request was throttled", response.data["detail"])
