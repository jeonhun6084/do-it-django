from django.urls import path, include
from . import views


urlpatterns = [
    path("search/<str:q>", views.PostSearch.as_view()),                  # 127.0.0.1/blog/search/1
    path("delete_comment/<int:pk>", views.delete_comment),               # 127.0.0.1/blog/delete_comment/1
    path("update_comment/<int:pk>", views.CommentUpdate.as_view()),      # 127.0.0.1/blog/update_comment/1
    path("update_post/<int:pk>", views.PostUpdate.as_view()),            # 127.0.0.1/blog/update_post/1
    path("create_post/", views.PostCreate.as_view()),                    # 127.0.0.1/blog/create_post/
    path("tag/<str:slug>", views.tag_page),                              # 127.0.0.1/blog/tag/경제
    path("category/<str:slug>", views.category_page),                    # 127.0.0.1/blog/category/경제
    path("<int:pk>/new_comment", views.new_comment),                     # 127.0.0.1/blog/1/new_comment
    path("<int:pk>", views.PostDetail.as_view()),                        # 127.0.0.1/blog/1
    path("", views.PostList.as_view())                                   # 127.0.0.1/blog/
]
