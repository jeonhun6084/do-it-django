from blog.models import Post, Category, Tag, Comment
from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup

# 테스트 클래스
class TestView(TestCase):
    # 테스트를 위한 초기 설정
    def setUp(self):
        # 테스트 클라이언트 초기화
        self.client = Client()

        # 'trump'라는 사용자 생성
        self.user_trump = User.objects.create_user(
            username='trump',
            password='1q2w3e4r!',  # 비밀번호 설정
        )

        # 여러 개의 포스트 생성
        self.post1 = Post.objects.create(
            title='가나다라',
            content='마바사',
            author=self.user_trump,
        )

        self.post2 = Post.objects.create(
            title='아자차카',
            content='타파하',
            author=self.user_trump,
        )

        self.post3 = Post.objects.create(
            title='가갸거겨고교',
            content='구규그기',
            author=self.user_trump,
        )

        self.post4 = Post.objects.create(
            title='나냐너녀노뇨',
            content='누뉴느니',
            author=self.user_trump,
        )

    # 'landing' 페이지의 테스트
    def test_landing(self):
        # 랜딩 페이지를 요청
        response = self.client.get('')
        
        # HTTP 응답 코드가 200(정상)인지 확인
        self.assertEqual(response.status_code, 200)
        
        # 응답된 HTML 페이지를 파싱
        bs = BeautifulSoup(response.content, 'lxml')

        # HTML body 부분을 추출
        body = bs.body
        
        # 첫 번째 포스트 제목('가나다라')는 랜딩 페이지에 있어서는 안됨
        self.assertNotIn(self.post1.title, body.text)
        
        # 두 번째, 세 번째, 네 번째 포스트 제목은 랜딩 페이지에 있어야 함
        self.assertIn(self.post2.title, body.text)
        self.assertIn(self.post3.title, body.text)
        self.assertIn(self.post4.title, body.text)
