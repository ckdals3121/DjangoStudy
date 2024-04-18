from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post

class TestView(TestCase) :
    def setUp(self) :
        self.client = Client()
        self.user_desmos = User.objects.create_user(username = "desmos", password = 'pass')
        self.user_mathway = User.objects.create_user(username = "mathway", password = "pass")

    def test_post_list(self) :
        # get post list 
        response = self.client.get('/blog/')
        # page load successfully
        self.assertEqual(response.status_code, 200)
        # page title is "Blog"
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, "Blog")
        # have nav bar, "Blog", "About Me" is in nav
        self.navbar_test(soup)

        # if there's no one Post
        self.assertEqual(Post.objects.count(), 0)
        # "아직 게시물이 없습니다" is in main area
        main_area = soup.find('div', id = "main-area")
        self.assertIn('아직 게시물이 없습니다', main_area.text)

        # it there are two Posts
        post_001 = Post.objects.create(
            title = "First Post",
            content = "Hello, It's First",
            author = self.user_desmos
        )
        post_002 = Post.objects.create(
            title = "Second Post",
            content = "Hello, It's Second",
            author = self.user_mathway
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

        # check author name
        self.assertIn(self.user_desmos.username.upper(), main_area.text)
        self.assertIn(self.user_mathway.username.upper(), main_area.text)

    def test_post_detail(self) :
        # There's one Post
        post_001 = Post.objects.create(
            title = "First Post",
            content = "It's First",
            author = self.user_desmos
        )
        # that Post's url is /blog/1
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # first post's detail page test
        # if get first post's content with url, it work correctly
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        # There's same nav bar 
        self.navbar_test(soup)
        # First post's title is in browser tab's title
        self.assertIn(post_001.title, soup.title.text)
        # First post's content is in post-area
        main_area = soup.find('div', id = "main-area")
        post_area = main_area.find('div', id = "post-area")
        self.assertIn(post_001.title, post_area.text)
        # First post's author is in post-area
        self.assertIn(self.user_desmos.username.upper(), post_area.text)
        # First post's content is in post-area
        self.assertIn(post_001.content, post_area.text)

    def navbar_test(self, soup) :
        navbar = soup.nav
        self.assertIn("Blog", navbar.text)
        self.assertIn("About Me", navbar.text)

        logo_btn = navbar.find('a', text = "Do It Django")
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text = "Home")
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text = 'Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text = 'About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')
