from django.urls import path
from . import views

urlpatterns = [
    #test page
    path('testpage/', views.test_page, name='test-page'),

    # journalist urls
    path('journalist/', views.journalist_dashboard_view, name='journalist-home'),
    path('journalist/dashboard', views.journalist_dashboard_view, name='journalist-dash'),
    path('journalist/article-list', views.journalist_article_list_view, name='journalist-article-list'),
    path('journalist/current-article', views.journalist_current_article_view, name='journalist-current-article'),
    path('journalist/submitted-articles', views.journalist_submitted_articles_view, name='journalist-submitted-articles'),
    path('journalist/reviews', views.journalist_reviews_view, name='journalist-reviews'),
    path('journalist/notifications', views.journalist_notifications_view, name='journalist-notifications'),
    path('journalist/messages', views.journalist_messages_view, name='journalist-messages'),
    path('journalist/profile-settings', views.journalist_profile_view, name='journalist-profile'),

    # Editor urls
    path('editor/', views.editor_dashboard_view, name='editor-home'),
    path('editor/dashboard', views.editor_dashboard_view, name='editor-dash'),
    path('editor/article-list', views.editor_article_list_view, name='editor-article-list'),
    path('editor/current-article', views.editor_current_article_view, name='editor-current-article'),
    path('editor/submitted-articles', views.editor_submitted_articles_view, name='editor-submitted-articles'),
    path('editor/reviews', views.editor_reviews_view, name='editor-reviews'),
    path('editor/notifications', views.editor_notifications_view, name='editor-notifications'),
    path('editor/messages', views.editor_messages_view, name='editor-messages'),
    path('editor/profile-settings', views.editor_profile_view, name='editor-profile'),


    # Director urls
    path('director/', views.director_dashboard_view, name='director-home'),
    path('director/dashboard', views.director_dashboard_view, name='director-dash'),
    path('director/article-list', views.director_article_list_view, name='director-article-list'),
    path('director/current-article', views.director_current_article_view, name='director-current-article'),
    path('director/submitted-articles', views.director_submitted_articles_view, name='director-submitted-articles'),
    path('director/reviews', views.director_reviews_view, name='director-reviews'),
    path('director/notifications', views.director_notifications_view, name='director-notifications'),
    path('director/messages', views.director_messages_view, name='director-messages'),
    path('director/profile-settings', views.director_profile_view, name='director-profile'),
]