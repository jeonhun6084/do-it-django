from django.shortcuts import render
from blog.models import Post

# landing 뷰 함수
# 최근 3개의 블로그 포스트를 가져와 'landing.html' 템플릿에 전달
def landing(request):
    # 최근 3개의 포스트를 가져오기
    recent_posts = Post.objects.order_by('-pk')[:3]

    # 'landing.html' 템플릿에 recent_posts 데이터를 전달하여 렌더링
    return render(
        request,
        "single_pages/landing.html",  # 템플릿 경로
        {
            'recent_posts': recent_posts  # 템플릿에 전달할 데이터
        }
    )

# about_me 뷰 함수
# 'about_me.html' 템플릿을 렌더링
def about_me(request):
    # 'about_me.html' 템플릿을 렌더링
    return render(
        request,
        "single_pages/about_me.html",  # 템플릿 경로
    )
