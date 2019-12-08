from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    # path('', views.post_list, name='post_list'),
    path('', views.PostList.as_view(), name='post_list'),
    # path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('search/', views.search, name='search'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    # path('post/new/', views.post_new, name='post_new'),
    path('post/new/', views.PostCreate.as_view(), name='post_new'),
    # path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/edit/', views.PostUpdate.as_view(), name='post_edit'),
    # path('post/post/<int:pk>/delete', views.post_remove, name='post_remove'),
    path('post/post/<int:pk>/delete', views.PostDelete.as_view(), name='post_remove'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('post/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('post/signup', views.signup, name='signup'),
]

