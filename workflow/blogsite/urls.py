from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_home_view, name='blog-home'),
    path('blog-home', views.blog_home_view, name='blog-home'),
    path('blog-list', views.blog_list_view, name='blog-list'),
    path('blog/<int:task_id>', views.blog_view, name='blog'),
    path('blog-preview/<int:task_id>', views.blog_preview, name='blog-preview'),
    path('contact-us', views.contact_us_view, name='contact-us'),
    path('about-us', views.about_us_view, name='about-us'),
]