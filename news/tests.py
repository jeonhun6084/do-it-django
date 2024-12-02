from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import NewsPost
# Create your tests here.


# class TestView(TestCase):
#     def setUp(self):
#         # 테스트를 실행하기 전에 Client 객체를 생성하여 요청을 보낼 준비를 합니다.
#         self.client = Client()

#     def test_post_list(self):
#         # 블로그 페이지에 GET 요청을 보내고 응답 상태 코드가 200인지 확인
#         response = self.client.get('/blog/')
#         self.assertEqual(response.status_code, 200)

#         # BeautifulSoup을 사용해 HTML을 파싱하고 title 태그의 내용을 확인
#         bs = BeautifulSoup(response.content, 'lxml')
#         self.assertEqual(bs.title.text, 'Blog')

#         # 네비게이션 바(nav) 내에 'Blog'와 'About Me' 링크가 있는지 확인
#         navbar = bs.nav
#         self.assertIn('Blog', navbar.text)
#         self.assertIn('About Me', navbar.text)

#         # 새로운 게시글 3개를 데이터베이스에 생성
#         post1 = Post.objects.create(
#             title='1',
#             content='1'
#         )
#         post2 = Post.objects.create(
#             title='2',
#             content='2'
#         )
#         post3 = Post.objects.create(
#             title='3',
#             content='3'
#         )

#         # 데이터베이스에 게시물이 3개가 맞는지 확인
#         self.assertEqual(Post.objects.count(), 3)

#         # 블로그 페이지에 다시 GET 요청을 보내고 응답 상태 코드가 200인지 확인
#         response = self.client.get('/blog/')
#         self.assertEqual(response.status_code, 200)

#         # BeautifulSoup을 사용해 HTML을 파싱하고 'main-area' div가 있는지 확인
#         bs = BeautifulSoup(response.content, 'lxml')

#         # 'main-area' div 안에 각 게시물의 제목이 포함되어 있는지 확인
#         main_area = bs.select('div#main-area')[0]
#         self.assertIn(post1.title, main_area.text)
#         self.assertIn(post2.title, main_area.text)
#         self.assertIn(post3.title, main_area.text)

#         # '아직 게시물이 없습니다.'라는 텍스트가 포함되지 않았는지 확인
#         self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

#     def test_post_detail(self):
#         post_001 = Post.objects.create(
#             title="첫 번째 포스트",
#             content="Hello world."
#         )
#         self.assertEqual(post_001.get_absolute_url(), '/blog/1')

#         response = self.client.get(post_001.get_absolute_url())
#         self.assertEqual(response.status_code, 200)
#         bs = BeautifulSoup(response.content, 'lxml')

#         navbar = bs.nav
#         self.assertIn('Blog', navbar.text)
#         self.assertIn('About Me', navbar.text)

#         self.assertIn(post_001.title, bs.title.text)

#         main_area = bs.select_one('div#main-area')
#         post_area = main_area.select_one('div#post-area')
#         self.assertIn(post_001.title, post_area.text)
#         self.assertIn(post_001.content, post_area.text)
