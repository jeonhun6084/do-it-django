from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Post, Category, Tag, Comment
from bs4 import BeautifulSoup

# 테스트 케이스 클래스 정의
class TestView(TestCase):
    def setUp(self):
        """
        테스트가 실행되기 전에 필요한 데이터와 객체들을 세팅합니다.
        - User 객체 생성 (트럼프, 오바마)
        - Category 객체 생성 (사회, 경제, 정치)
        - Tag 객체 생성 (파이썬 공부, python, hello)
        - Post 객체 3개 생성 (각각 트럼프와 오바마 작성)
        - 각 게시물에 댓글 추가
        """
        self.client = Client()

        # 사용자 생성 (트럼프와 오바마)
        self.user_trump = User.objects.create_user(
            username='trump',
            password='1q2w3e4r!',
        )
        self.user_trump.is_staff = True  # 트럼프는 관리자 권한을 가진 사용자
        self.user_trump.save()
        self.user_obama = User.objects.create_user(
            username='obama',
            password='1q2w3e4r!',
        )

        # 카테고리 생성 (사회, 경제, 정치)
        self.category_society = Category.objects.create(
            name='society',
            slug='society',
        )
        self.category_economy = Category.objects.create(
            name='economy',
            slug='economy',
        )
        self.category_politic = Category.objects.create(
            name='politic',
            slug='politic',
        )

        # 태그 생성 (파이썬 공부, python, hello)
        self.tag_python_kor = Tag.objects.create(
            name='파이썬 공부',
            slug='파이썬-공부',
        )
        self.tag_python = Tag.objects.create(
            name='python',
            slug='python',
        )
        self.tag_hello = Tag.objects.create(
            name='hello',
            slug='hello',
        )

        # 게시물 생성 (트럼프와 오바마가 작성한 게시물 3개)
        self.post1 = Post.objects.create(
            title='가나다라',
            content='마바사',
            author=self.user_trump,
            category=self.category_politic,
        )
        self.post1.tags.add(self.tag_hello)  # 첫 번째 게시물에 'hello' 태그 추가

        # 첫 번째 게시물에 댓글 추가
        self.comment1 = Comment.objects.create(
            post=self.post1,
            author=self.user_obama,
            content='첫 번째 댓글',
        )

        # 두 번째 게시물 (오바마는 카테고리 없이 작성)
        self.post2 = Post.objects.create(
            title='아자차카',
            content='타파하',
            author=self.user_trump,
            category=self.category_economy,
        )

        # 세 번째 게시물 (트럼프가 '파이썬 공부'와 'python' 태그를 추가)
        self.post3 = Post.objects.create(
            title='가갸거겨고교',
            content='구규그기',
            author=self.user_obama,
        )
        self.post3.tags.add(self.tag_python_kor)
        self.post3.tags.add(self.tag_python)

    def category_card_test(self, bs):
        """
        카테고리 카드 영역에 대해 테스트합니다.
        - 각 카테고리 이름과 해당 카테고리의 게시물 수가 올바르게 표시되는지 검증
        """
        categories_card = bs.select_one('div#categories-card')

        # 'Categories' 텍스트가 포함되어 있는지 확인
        self.assertIn('Categories', categories_card.text)

        # 각 카테고리별 게시물 수가 정확히 출력되는지 확인
        self.assertIn(f'{self.category_economy.name} ({self.category_economy.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_politic.name} ({self.category_politic.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_society.name} ({self.category_society.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)

    def test_navbar(self):
        """
        블로그의 네비게이션 바(nav)에 'Blog'와 'About Me' 링크가 포함되어 있는지 확인합니다.
        """
        # 블로그 메인 페이지로 GET 요청
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        # BeautifulSoup을 사용해 HTML을 파싱하고 title 태그의 내용을 확인
        bs = BeautifulSoup(response.content, 'lxml')
        self.assertEqual(bs.title.text, 'Blog')

        # 네비게이션 바(nav) 내에 'Blog'와 'About Me' 링크가 포함되어 있는지 확인
        navbar = bs.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

    def test_post_list(self):
        """
        블로그 페이지에 표시된 게시물 목록이 올바른지 테스트합니다.
        - 각 게시물의 제목, 카테고리, 태그가 올바르게 출력되는지 확인
        """
        # 데이터베이스에 게시물이 3개가 맞는지 확인
        self.assertEqual(Post.objects.count(), 3)

        # 블로그 페이지로 다시 GET 요청
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        # BeautifulSoup을 사용해 HTML을 파싱
        bs = BeautifulSoup(response.content, 'lxml')

        # 카테고리 카드 영역 테스트
        self.category_card_test(bs)

        # 게시물 목록을 담고 있는 'main-area' div를 선택
        main_area = bs.select('div#main-area')[0]

        # 게시물이 없을 때 표시되는 텍스트가 나타나지 않도록 확인
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        # 첫 번째 게시물의 카드가 올바르게 렌더링되는지 확인
        post1_card = main_area.select_one('div#post-1')
        self.assertIn(self.post1.title, post1_card.text)
        self.assertIn(self.post1.category.name, post1_card.text)
        self.assertIn(self.tag_hello.name, post1_card.text)
        self.assertNotIn(self.tag_python_kor.name, post1_card.text)
        self.assertNotIn(self.tag_python.name, post1_card.text)

        # 두 번째 게시물
        post2_card = main_area.select_one('div#post-2')
        self.assertIn(self.post2.title, post2_card.text)
        self.assertIn(self.post2.category.name, post2_card.text)
        self.assertNotIn(self.tag_hello.name, post2_card.text)
        self.assertNotIn(self.tag_python_kor.name, post2_card.text)
        self.assertNotIn(self.tag_python.name, post2_card.text)

        # 세 번째 게시물
        post3_card = main_area.select_one('div#post-3')
        self.assertIn(self.post3.title, post3_card.text)
        self.assertIsNone(self.post3.category)
        self.assertNotIn(self.tag_hello.name, post3_card.text)
        self.assertIn(self.tag_python_kor.name, post3_card.text)
        self.assertIn(self.tag_python.name, post3_card.text)

        # 게시물에 작성한 사용자 이름이 표시되는지 확인
        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

        # 게시물이 없을 때 테스트
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        # 게시물이 없을 때 '아직 게시물이 없습니다.' 텍스트가 나타나는지 확인
        bs = BeautifulSoup(response.content, 'lxml')
        main_area = bs.select('div#main-area')[0]
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

    def test_post_detail(self):
        """
        게시물 상세 페이지에서 게시물 내용, 작성자, 카테고리, 댓글 등의 정보가 올바르게 표시되는지 테스트합니다.
        """
        # 게시물의 절대 URL이 올바르게 생성되는지 확인
        self.assertEqual(self.post1.get_absolute_url(), '/blog/1')

        # 게시물 상세 페이지로 GET 요청
        response = self.client.get(self.post1.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        # BeautifulSoup을 사용해 HTML을 파싱
        bs = BeautifulSoup(response.content, 'lxml')

        # 카테고리 카드 영역 테스트
        self.category_card_test(bs)

        # 게시물 내용이 'post-area'에 포함되어 있는지 확인
        main_area = bs.select_one('div#main-area')
        post_area = main_area.select_one('div#post-area')
        self.assertIn(self.post1.title, post_area.text)
        self.assertIn(self.category_politic.name, post_area.text)

        # 작성자 정보가 포함되어 있는지 확인
        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.post1.content, post_area.text)

        # 댓글 영역 확인
        comment_area = bs.select_one('div#comment-area')
        comment1_area = comment_area.select_one('div#comment-1')
        self.assertIn(self.comment1.author.username, comment1_area.text)
        self.assertIn(self.comment1.content, comment1_area.text)

    def test_category_page(self):
        """
        카테고리 페이지에서 해당 카테고리의 게시물들이 잘 출력되는지 테스트합니다.
        """
        # 특정 카테고리(정치)에 대한 페이지로 GET 요청
        response = self.client.get(self.category_politic.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        bs = BeautifulSoup(response.content, 'lxml')
        self.category_card_test(bs)

        # 페이지 제목이 해당 카테고리 이름을 포함하는지 확인
        self.assertIn(self.category_politic.name, bs.h1.text)

        main_area = bs.select_one('div#main-area')
        # 카테고리 이름과 게시물 제목이 포함되어 있는지 확인
        self.assertIn(self.category_politic.name, main_area.text)
        self.assertIn(self.post1.title, main_area.text)

    def test_tag_page(self):
        """
        태그 페이지에서 해당 태그가 포함된 게시물들이 잘 출력되는지 테스트합니다.
        """
        # 특정 태그(hello)에 대한 페이지로 GET 요청
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        bs = BeautifulSoup(response.content, 'lxml')
        self.category_card_test(bs)

        # 페이지 제목이 해당 태그 이름을 포함하는지 확인
        self.assertIn(self.tag_hello.name, bs.h1.text)

        main_area = bs.select_one('div#main-area')
        # 해당 태그가 포함된 게시물이 잘 출력되는지 확인
        self.assertIn(self.tag_hello.name, main_area.text)
        self.assertIn(self.post1.title, main_area.text)
        self.assertNotIn(self.post2.title, main_area.text)
        self.assertNotIn(self.post3.title, main_area.text)

    def test_create_post(self):
        """
        게시물 생성 기능을 테스트합니다. 사용자가 새로운 게시물을 작성할 수 있는지, 태그 추가가 가능한지 확인합니다.
        """
        # 게시물 생성 페이지에 접근하려면 로그인된 상태여야 하므로 비로그인 상태에서는 접근이 불가함을 확인
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)  # 비로그인 상태에서 200 응답이 나오지 않음

        # 오바마 계정으로 로그인 후 게시물 생성 페이지로 접근
        self.client.login(username='obama', password='1q2w3e4r!')
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        
        # 폼에 새 게시물 데이터를 POST로 전송하여 생성되는지 확인
        response = self.client.post('/blog/create_post/', {
            'title': '새 게시물',
            'content': '새로운 게시물의 내용입니다.',
            'category': self.category_society.id,
            'tags': [self.tag_python.id],
        })
        self.assertEqual(response.status_code, 302)  # 정상적으로 게시물 생성 후 리디렉션

        # 새 게시물이 생성되었는지 확인
        self.assertEqual(Post.objects.count(), 4)
        new_post = Post.objects.latest('created_at')
        self.assertEqual(new_post.title, '새 게시물')
        self.assertIn(self.tag_python, new_post.tags.all())
