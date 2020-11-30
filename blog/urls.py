from django.urls import path

from blog import views as blog_view


urlpatterns = [
    path('', blog_view.index, name='blog-index'),
    path('category/<str:category>/', blog_view.category, name='blog-category'),
    path('dashboard/', blog_view.dashboard, name='blog-dashboard'),
    path('post/create/', blog_view.create_post, name='blog-create-post'),
    path('post/edit/<str:slug>/', blog_view.edit_post, name='blog-edit-post'),
    path('post/delete/<int:pk>/', blog_view.delete_post, name='blog-delete-post'),
    path('<str:slug>/', blog_view.blog_post, name='blog-post'),
]
