from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .models import Post, Category, Tag, Comment
from .forms import CommentForm

# 특정 태그에 해당하는 포스트들을 표시하는 함수형 뷰
def tag_page(request, slug):
    # slug를 기반으로 태그 객체를 가져옴
    tag = Tag.objects.get(slug=slug)
    # 해당 태그와 연관된 모든 포스트를 가져옴
    post_list = tag.post_set.all()

    # 'post_list.html' 템플릿을 렌더링하며, 태그와 포스트 리스트를 포함한 다른 데이터를 전달
    return render(
        request,
        "blog/post_list.html",
        {
            "post_list": post_list,  # 선택된 태그와 관련된 포스트 리스트
            "categories": Category.objects.all(),  # 사이드바에 표시될 카테고리들
            "no_category_post_count": Post.objects.filter(category=None).count(),  # 카테고리가 없는 포스트 수
            "tag": tag,  # 현재 선택된 태그
        }
    )

# 특정 카테고리에 해당하는 포스트들을 표시하는 함수형 뷰
def category_page(request, slug):
    # 'no_category' 슬러그일 경우, 카테고리가 없는 포스트들만 가져옴
    if slug == 'no_category':
        category = '미분류'  # 카테고리가 없는 포스트들은 '미분류'로 표시
        post_list = Post.objects.filter(category=None)  # 카테고리가 없는 포스트들
    else:
        # 슬러그를 기반으로 카테고리 객체를 가져옴
        category = Category.objects.get(slug=slug)
        # 해당 카테고리에 속한 포스트들을 가져옴
        post_list = Post.objects.filter(category=category)

    # 'post_list.html' 템플릿을 렌더링하며, 카테고리와 포스트 리스트를 포함한 다른 데이터를 전달
    return render(
        request,
        "blog/post_list.html",
        {
            "post_list": post_list,  # 선택된 카테고리와 관련된 포스트 리스트
            "categories": Category.objects.all(),  # 사이드바에 표시될 카테고리들
            "no_category_post_count": Post.objects.filter(category=None).count(),  # 카테고리가 없는 포스트 수
            "category": category,  # 현재 선택된 카테고리
        }
    )

# 포스트 리스트를 보여주는 클래스 기반 뷰
class PostList(ListView):
    model = Post
    ordering = "-pk"  # 포스트를 최신 순으로 정렬
    paginate_by = 5  # 페이지당 5개 포스트씩 표시

    # 템플릿에 추가적인 데이터를 전달하는 메서드
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 카테고리와 카테고리가 없는 포스트 수를 추가하여 전달
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context

# 특정 포스트의 상세 정보를 보여주는 클래스 기반 뷰
class PostDetail(DetailView):
    model = Post

    # 템플릿에 추가적인 데이터를 전달하는 메서드
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 카테고리와 카테고리가 없는 포스트 수, 댓글 폼을 추가하여 전달
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm

        return context

# 새 포스트를 작성하는 클래스 기반 뷰
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    # 포스트 작성 권한을 슈퍼유저 또는 스태프만 할 수 있도록 제한
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    # 폼이 유효하면 추가적인 작업을 수행하는 메서드
    def form_valid(self, form):
        current_user = self.request.user

        # 인증된 사용자이고, 스태프 또는 슈퍼유저일 경우에만 포스트를 작성하도록 설정
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user  # 현재 사용자를 작성자로 설정
            response = super().form_valid(form)

            # 태그 입력값을 받아 포스트에 추가하는 작업
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()  # 공백 제거
                tags_str = tags_str.replace(',', ';')  # 콤마를 세미콜론으로 변경
                tags = tags_str.split(';')  # 세미콜론을 기준으로 태그 분리

                # 각 태그에 대해 기존 태그를 찾거나 새로운 태그를 생성하고 포스트에 추가
                for tag in tags:
                    tag = tag.strip()  # 각 태그의 공백 제거
                    tag_obj = Tag.objects.filter(name=tag).first()  # 이미 존재하는 태그 확인

                    if not tag_obj:
                        # 태그가 없으면 새로 생성
                        slug = slugify(tag, allow_unicode=True)
                        tag_obj = Tag.objects.create(name=tag, slug=slug)
                    
                    self.object.tags.add(tag_obj)  # 포스트에 태그 추가

            return response

    def handle_no_permission(self):
        # 권한이 없는 경우 블로그 메인 페이지로 리디렉션
        return redirect('/blog/')

# 기존 포스트를 수정하는 클래스 기반 뷰
class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    template_name = 'blog/post_update_form.html'

    # 포스트 수정 권한을 슈퍼유저, 스태프, 또는 포스트 작성자만 할 수 있도록 제한
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    # 포스트 작성자만 수정할 수 있도록 하는 메서드
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied  # 작성자가 아니면 접근을 거부

    # 템플릿에 추가적인 데이터를 전달하는 메서드
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 포스트에 기존 태그가 있으면 태그를 세미콜론으로 구분하여 기본값으로 설정
        if self.object.tags.exists():
            tags = list()
            for tag in self.object.tags.all():
                tags.append(tag.name)
            
            context['tags_str_default'] = '; '.join(tags)  # 태그를 세미콜론으로 구분하여 전달

        return context

    # 폼이 유효하면 추가적인 작업을 수행하는 메서드
    def form_valid(self, form):
        current_user = self.request.user

        # 인증된 사용자이고, 스태프 또는 슈퍼유저일 경우에만 포스트를 수정하도록 설정
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user  # 현재 사용자를 작성자로 설정
            response = super().form_valid(form)

            # 태그 입력값을 받아 포스트에 추가하는 작업
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()  # 공백 제거
                tags_str = tags_str.replace(',', ';')  # 콤마를 세미콜론으로 변경
                tags = tags_str.split(';')  # 세미콜론을 기준으로 태그 분리

                # 각 태그에 대해 기존 태그를 찾거나 새로운 태그를 생성하고 포스트에 추가
                for tag in tags:
                    tag = tag.strip()  # 각 태그의 공백 제거
                    tag_obj = Tag.objects.filter(name=tag).first()  # 이미 존재하는 태그 확인

                    if not tag_obj:
                        # 태그가 없으면 새로 생성
                        slug = slugify(tag, allow_unicode=True)
                        tag_obj = Tag.objects.create(name=tag, slug=slug)
                    
                    self.object.tags.add(tag_obj)  # 포스트에 태그 추가

            return response


# 댓글을 새로 작성하는 뷰 함수
def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()

                return redirect(comment.get_absolute_url())

        else:
            return redirect(post.get_absolute_url())
    
    else:
        raise PermissionDenied


# 댓글을 수정하는 클래스 기반 뷰
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    
    # 댓글 수정 권한을 슈퍼유저, 스태프, 또는 댓글 작성자만 할 수 있도록 제한
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    # 댓글 작성자만 수정할 수 있도록 하는 메서드
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied  # 작성자가 아니면 접근을 거부


# 댓글을 삭제하는 뷰 함수
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post

    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        
        return redirect(post.get_absolute_url())   
    else:
        raise PermissionDenied


# 포스트를 검색하는 클래스 기반 뷰
class PostSearch(PostList):
    paginate_by = None

    # 검색어를 기반으로 포스트를 검색하는 메서드
    def get_queryset(self):
        q = self.kwargs.get('q')
        post_list = Post.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()

        return post_list
    
    # 검색 결과와 함께 검색 정보를 추가하는 메서드
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.kwargs.get('q')
        context['search_info'] = f'검색: {q} ({self.get_queryset().count()})'

        return context
