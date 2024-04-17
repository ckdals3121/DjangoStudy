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

    def test_post_detail(self) :
        # There's one Post
        post_001 = Post.objects.create(
            title = "First Post",
            content = "It's First",
        )
        # that Post's url is /blog/1
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # first post's detail page test
        # if get first post's content with url, it work correctly
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        # There's same nav bar 
        navbar = soup.nav
        self.assertIn("Blog", navbar.text)
        self.assertIn("About Me", navbar.text)
        # First post's title is in browser tab's title
        self.assertIn(post_001.title, soup.title.text)
        # First post's content is in post-area
        main_area = soup.find('div', id = "main-area")
        post_area = main_area.find('div', id = "post-area")
        self.assertIn(post_001.title, post_area.text)
        # First post's author is in post-area

        # First post's content is in post-area
        self.assertIn(post_001.content, post_area.text)
