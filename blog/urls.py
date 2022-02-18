from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('post/<int:post_id>/', views.view_post, name='blog-post'),
    path('my-posts/', views.posts_list, name='blog-posts-list'),
    path('create-post/', views.add_post, name='create-post'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='update-post'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete-post')
]
