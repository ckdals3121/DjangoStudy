from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

class TestView(TestCase) :
    def setUp(self) :
        self.client = Client()

    def test_post_list(self) :
        # get post list 
        response = self.client.get('/blog/')
        # page load successfully
        self.assertEqual(response.status_code, 200)
        # page title is "Blog"
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, "Blog")
        # have nav bar
        navbar = soup.nav
        # "Blog", "About Me" is in nav
        self.assertIn("Blog", navbar.text)
        self.assertIn("About Me", navbar.text)

        # if there's no one Post
        self.assertEqual(Post.objects.count(), 0)
        # "아직 게시물이 없습니다" is in main area
        main_area = soup.find('div', id = "main-area")
        self.assertIn('아직 게시물이 없습니다', main_area.text)

        # it there are two Posts
        post_001 = Post.objects.create(
            title = "First Post",
            content = "Hello, It's First",
        )
        post_002 = Post.objects.create(
            title = "Second Post",
            content = "Hello, It's Second",
        )
        self.assertEqual(Post.objects.count(), 2)

        # if refresh post list page
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        # there are two Post titles in main area
        main_area = soup.find('div', id = "main-area")
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # there's no "아직 게시물이 없습니다"
        self.assertNotIn("아직 게시물이 없습니다", main_area.text)