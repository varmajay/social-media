from django.contrib import admin
from django.urls import path
from .import views
from django.urls import reverse


urlpatterns = [
    path('index/',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('setting/',views.setting,name='setting'),
    path('profile/',views.profile,name='profile'),
    path('edit-profile/',views.edit_profile,name='edit-profile'),
    path('search/',views.search,name='search'),
    path('edit-post/<int:pk>',views.edit_post,name='edit-post'),
    path('delete-post/<int:pk>',views.delete_post,name='delete-post'),
    path('view-profile/<int:pk>',views.view_profile,name='view-profile'),
    path('follow/',views.follow,name='follow'),
    path('like-post-profile', views.like_post_profile, name='like-post-profile'),
    path('like-post', views.like_post, name='like-post'),
    path('comment/<int:pk>',views.comment, name='comment'),
    path('view-comment/<int:pk>',views.view_comment, name='view-comment'),

]