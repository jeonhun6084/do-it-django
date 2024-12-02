from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import NewsPost, Press

# Create your views here.
# def index(reqeust):
#     posts = Post.objects.all().order_by('-pk')

#     return render(
#         reqeust,
#         "news/index.html",
#         {
#             "posts": posts,
#         }
#     )


# def single_post_page(reqeust, pk):
#     post = Post.objects.get(pk=pk)

#     return render(
#         reqeust,
#         "news/single_post_page.html",
#         {
#             "post": post,
#         }
#     )


def category_page(reqeust, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = NewsPost.objects.filter(category=None)
    else:
        category = Press.objects.get(slug=slug)
        post_list = NewsPost.objects.filter(category=category)

    return render(
        reqeust,
        "news/post_list.html",
        {
            "post_list": post_list,
            "categories": Press.objects.all(),
            "no_category_post_count": NewsPost.objects.filter(category=None).count(),
            "category": category,
        }
    )


class PostList(ListView):
    model = NewsPost
    ordering = "-pk"

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Press.objects.all()
        context['no_category_post_count'] = NewsPost.objects.filter(category=None).count()

        return context


class PostDetail(DetailView):
    model = NewsPost

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Press.objects.all()
        context['no_category_post_count'] = NewsPost.objects.filter(category=None).count()

        return context
