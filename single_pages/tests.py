from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from blog.models import Post

class TestView(TestCase) :
    def setUp(self) :
        self.client = Client()
        self.user_desmos = User.objects.create_user(username = "desmos", password = "pass")

    def test_landing(self) :
        post_001 = Post.objects.create(
            title = "첫 번째 포스트",
            content = "첫 번째 포스트입니다.",
            author = self.user_desmos
        )

        post_002 = Post.objects.create(
            title = "두 번째 포스트",
            content = "두 번째 포스트입니다.",
            author = self.user_desmos
        )

        post_003 = Post.objects.create(
            title = "세 번째 포스트",
            content = "세 번째 포스트입니다.",
            author = self.user_desmos
        )

        post_004 = Post.objects.create(
            title = "네 번째 포스트",
            content = "네 번째 포스트입니다.",
            author = self.user_desmos
        )

        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        body = soup.body
        self.assertNotIn(post_001.title, body.text)
        self.assertIn(post_002.title, body.text)
        self.assertIn(post_003.title, body.text)
        self.assertIn(post_004.title, body.text)