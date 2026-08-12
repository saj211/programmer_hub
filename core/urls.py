from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),                    
    path('register/', views.register_view, name='register'),   
    path('login/', views.login_view, name='login'),   

path(
    'password_reset/',
    auth_views.PasswordResetView.as_view(
        template_name='core/registration/password_reset_form.html',
        email_template_name='core/registration/password_reset_email.html',
    ),
    name='password_reset_form',
),

path(
    'password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(
        template_name='core/registration/password_reset_done.html',
    ),
    name='password_reset_done',
),

path(
    'reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='core/registration/password_reset_confirm.html',
    ),
    name='password_reset_confirm',
),

path(
    'reset/done/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='core/registration/password_reset_complete.html',
    ),
    name='password_reset_complete',
),

    path('logout/', views.logout_view, name='logout'),         
    path('profile/<str:username>/', views.profile_view, name='profile'),  
    path('profile/<str:username>/edit/',views.edit_profile_view,name='edit_profile'),
    path('chat/', views.chat_list_view, name='chat_list'),
    path('chat/<int:user_id>/', views.chat_detail_view, name='chat_detail'),
    path('posts/create/', views.create_post, name='create_post'),
    path('post_list/', views.post_list_view, name='post_list'),
    path('posts/<int:post_id>/edit/',views.edit_post,name='edit_post'),
    path('posts/<int:post_id>/delete/',views.delete_post,name='delete_post'),
]