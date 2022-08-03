from django.urls import path

from django.contrib.auth import views as auth_views

from .import views

from .views import TagsCreateView

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('add_tags/', views.addtags, name="add_tags"),
    path('add_image/', views.addimage, name="add_image"),


    path('', views.posts, name='posts'),#posts, home
    path('contact/', views.contact, name='contact'),
    # path('services/', views.services, name='services'),
    # path('posts/', views.posts, name='posts'),
	path('post/<slug:slug>/', views.post, name="post"),
    path('gallery/', views.gallery, name='gallery'),

    #CRUD PATHS
	path('create_post/', views.createPost, name="create_post"),
    path('update_post/<slug:slug>/', views.updatePost, name="update_post"),
    path('delete_post/<slug:slug>/', views.deletePost, name="delete_post"),


    path('send_email/', views.sendEmail, name="send_email"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="base/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="base/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="base/password_reset_done.html"), name="password_reset_complete"),

    
]

