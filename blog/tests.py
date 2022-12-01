from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category

class TestView(TestCase) :
    def setUp(self) :
        self.client = Client()
        self.user_trump = User.objects.create_user(
            username='trump', password='somepassword'
        )
        self.user_obama = User.objects.create_user(
            username='obama', password='somepassword'
        )

        self.category_programming = Category.objects.create(name="programming",
                                                            slug="programming")
        self.category_music = Category.objects.create(name="music",
                                                            slug="music")

        self.post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='하하하하히히히히히',
            category=self.category_programming,
            author=self.user_trump
        )
        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='후후후후후햐햐햐햐햐ㅇ아아아아아아아아아아',
            category=self.category_music,
            author=self.user_obama
        )
        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content='카테고리가 없을 수도~',
            author=self.user_obama
        )

    def category_card_test(self, soup) :
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text='MR CLASS')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')



    def test_post_list(self):
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)


    def test_post_detail(self):
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='TDD... 맘에 안 드는 단어야',
            author=self.user_trump
        )
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)

        self.assertIn(post_001.title, soup.title.text)

        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)
        self.assertIn(self.user_trump.username.upper(), post_area.text)
        self.assertIn(post_001.content, post_area.text)



# from django.test import TestCase, Client
# from bs4 import BeautifulSoup
# from django.contrib.auth.models import User
# from .models import Post, Category
#
# class TestView(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user_trump = User.objects.create_user(username='trump', password='somepassword')
#         self.user_obama = User.objects.create_user(username='obama', password='somepassword')
#
#         self.category_programming = Category.objects.create(name='programming', slug='programming')
#         self.category_music = Category.objects.create(name='music', slug='music')
#
#         self.post_001 = Post.objects.create(
#             title='첫 번째 포스트입니다.',
#             content='Hello World. We are the world.',
#             category=self.category_programming,
#             author=self.user_trump
#         )
#         self.post_002 = Post.objects.create(
#             title='두 번째 포스트입니다.',
#             content='1등이 전부는 아니잖아요?',
#             category=self.category_music,
#             author=self.user_obama
#         )
#         self.post_003 = Post.objects.create(
#             title='세 번째 포스트입니다.',
#             content='Category가 없을 수도 있죠',
#             category=self.category_programming,
#             author=self.user_obama
#         )
#
#     def category_card_test(self, soup) :
#         categories_card = soup.find('div', id='categories-card')
#         self.assertIn('Categories', categories_card.text)
#         self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)
#         self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
#         self.assertIn(f'미분류 (1)', categories_card.text)
#
#     def navbar_test(self, soup):
#         navbar = soup.nav
#         self.assertIn('Blog', navbar.text)
#         self.assertIn('About Me', navbar.text)
#
#         logo_btn = navbar.find('a', text='MR CLASS')
#         self.assertEqual(logo_btn.attrs['href'], '/')
#
#         home_btn = navbar.find('a', text="Home")
#         self.assertEqual(home_btn.attrs['href'], '/')
#
#         blog_btn = navbar.find('a', text="Blog")
#         self.assertEqual(blog_btn.attrs['href'], '/blog/')
#
#         about_me_btn = navbar.find('a', text="About Me")
#         self.assertEqual(about_me_btn.attrs['href'], '/about_me/')
#
#     # 이전 코드 (삭제 대신 주석 처리함)
#     # def test_post_list(self):
#     #     # 1.1.포스트 목록 페이지를 가져온다.
#     #     response = self.client.get('/blog/')
#     #     # 1.2. 정상적으로 페이지가 로드된다.
#     #     self.assertEqual(response.status_code, 200)
#     #     # 1.3. 페이지 타이틀은 'Blog'이다.
#     #     soup = BeautifulSoup(response.content, 'html.parser')
#     #     self.assertEqual(soup.title.text, 'Blog')
#     #     # 1.4. navbar_test를 호출한다.
#     #     self.navbar_test(soup)
#     #
#     #     #2.1. 포스트(게시물)가 하나도 없다면
#     #     self.assertEqual(Post.objects.count(), 0)
#     #     # 2.2. main area에 '아직 게시물이 없습니다.'라는 문구가 나타난다.
#     #     main_area = soup.find('div', id='main-area')
#     #     self.assertIn('아직 게시물이 없습니다.', main_area.text) # 우리는 여기서 에러가 날 것을 기대
#     #
#     #     # 3.1. 포스트가 2개 있다면
#     #     post_001 = Post.objects.create(
#     #         title='첫 번째 포스트입니다.',
#     #         content='Hellow World. We are the world.',
#     #         author=self.user_trump
#     #     )
#     #     post_002 = Post.objects.create(
#     #         title='두 번째 포스트입니다.',
#     #         content='1등이 전부는 아니잖아요?',
#     #         author=self.user_obama
#     #     )
#     #     self.assertEqual(Post.objects.count(), 2)
#     #
#     #     # 3.2. 포스트 목록 페이지를 새로고침했을 때
#     #     response = self.client.get('/blog/')
#     #     soup = BeautifulSoup(response.content, 'html.parser')
#     #     self.assertEqual(response.status_code, 200)
#     #     # 3.3. main area에 포스트 2개의 제목이 존재한다.
#     #     main_area = soup.find('div', id='main-area')
#     #     self.assertIn(post_001.title, main_area.text)
#     #     self.assertIn(post_002.title, main_area.text)
#     #     #3.4. '아직 게시물이 없습니다.'라는 문구는 더이상 나타나지 않는다.
#     #     self.assertNotIn('아직 게시물이 없습니다.', main_area.text)
#     #
#     #     self.assertIn(self.user_trump.username.upper(), main_area.text)
#     #     self.assertIn(self.user_obama.username.upper(), main_area.text)
#
#     def test_post_list(self):
#         # 포스트가 있는 경우
#         self.assertEqual(Post.objects.count(), 3)
#
#         response = self.client.get('/blog/')
#         self.assertEqual(response.status_code, 200)
#         soup = BeautifulSoup(response.content, 'html.parser')
#
#         self.navbar_test(soup)
#         self.category_card_test(soup)
#
#         main_area = soup.find('div', id='main-area')
#         self.assertNotIn('아직 게시글이 없습니다.', main_area.text)
#
#         post_001_card = main_area.find('div', id='post-1')
#         self.assertIn(self.post_001.title, post_001_card.text)
#         self.assertIn(self.post_001.category.name, post_001_card.text)
#
#         post_002_card = main_area.find('div', id='post-2')
#         self.assertIn(self.post_002.title, post_002_card.text)
#         self.assertIn(self.post_002.category.name, post_002_card.text)
#
#         post_003_card = main_area.find('div', id='post-3')
#         self.assertIn('미분류', post_003_card.text)
#         self.assertIn(self.post_003.category.name, post_003_card.text)
#
#         self.assertIn(self.user_trump.username.upper(), main_area.text)
#         self.assertIn(self.user_obama.username.upper(), main_area.text)
#
#         # 포스트가 없는 경우
#         Post.objrcts.all().delete()
#         self.assertEqual(Post.objects.count(), 0)
#         response = self.client.get('/blog/')
#         soup = BeautifulSoup(response.content, 'html.parser')
#
#         main_area = soup.find('div', id='main-area')
#         self.assertIn('아직 게시물이 없습니다.', main_area.text)
#
#
#     def test_post_detail(self):
#         # 1.1. Post가 하나 있다.
#         post_001 = Post.objects.create(
#             title='첫 번째 포스트입니다.',
#             content='Hello World. We are the world.',
#             author=self.user_trump,
#         )
#         #1.2. 그 포스트의 url은 'blog/1/'이다.
#         self.assertEqual(post_001.get_absolute_url(), '/blog/1/')
#
#         # 2. 펏 번째 포스틑의 상세 페이지 테스트
#         # 2.1. 첫 번째 post url로 접근하면 정상적으로 작동한다(status code: 200)
#         response = self.client.get(post_001.get_absolute_url())
#         self.assertEqual(response.status_code, 200)
#         soup = BeautifulSoup(response.content, 'html.parser')
#
#         # 2.2. 포스트 목록 페이지와 같은 내비게이션 바가 있다. navbar_test을 호출한다.
#         self.navbar_test(soup)
#
#         # 2.3. 첫 번째 포스트의 제목(title)이 웹 브라우저 탭 타이틀에 들어 있다.
#         self.assertIn(post_001.title, soup.title.text)
#
#         # 2.4. 첫 번째 포스트의 제목이 포스트 영역(post_area)에 있다.
#         main_area = soup.find('div', id='main-area')
#         post_area = main_area.find('div', id='post-area')
#         self.assertIn(post_001.title, post_area.text)
#
#         # 2.5. 첫 번째 포스트 작성자(author)가 포스트 영역에 있다.
#         self.assertIn(self.user_trump.username.upper(), post_area.text)
#
#         # 2.6. 첫 번째 포스트의 내용(content)이 포스트 영역에 있다.
#         self.assertIn(post_001.content, post_area.text)
