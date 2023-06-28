from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import CapacityChoices

#Journalist Views

@login_required
def test_page(request):
    context={}
    return render(request, "testpage.html", context)

@login_required
def login_redirect(request):
    user = request.user
    capacity = user.profile.capacity
    print(capacity)
    print(user.profile.id_card_number)

    if capacity == CapacityChoices.WRITER:
        return redirect('journalist-home')
    elif capacity == CapacityChoices.PHOTOJOURNALIST:
        return redirect('journalist-home')
    elif capacity == CapacityChoices.EDITOR:
        return redirect('editor-home')
    elif capacity == CapacityChoices.DIRECTOR:
        return redirect('director-home')
    else:
        return redirect('logout')


@login_required
def journalist_dashboard_view(request):
    context={}
    context['page_title'] = 'Dashboard' 
    return render(request, "journalist/dashboard.html", context)

@login_required
def journalist_article_list_view(request):
    context={}
    context['page_title'] = 'Articles List'

    
    return render(request, "journalist/article-list.html", context)

@login_required
def journalist_current_article_view(request):
    context={}
    context['page_title'] = 'Article'
    user = request.user
    capacity = user.profile.capacity
    # If statemtn for usertype to go to current-article-2
    if capacity == CapacityChoices.WRITER:
        return render(request, "journalist/current-article.html", context)
    elif capacity == CapacityChoices.PHOTOJOURNALIST:
        return render(request, "journalist/current-article-2.html", context)

@login_required
def journalist_reviews_view(request):
    context={}
    context['page_title'] = 'Reviews'
    return render(request, "journalist/reviews.html", context)

@login_required
def journalist_submitted_articles_view(request):
    context={}
    context['page_title'] = 'Article Feedback'
    return render(request, "journalist/submitted-articles.html", context)

@login_required
def journalist_messages_view(request):
    context={}
    return render(request, "journalist/messages.html", context)

@login_required
def journalist_notifications_view(request):
    context={}
    context['page_title'] = 'Notifications'
    return render(request, "journalist/notifications.html", context)

@login_required
def journalist_profile_view(request):
    context={}
    context['page_title'] = 'Profile Settings'
    return render(request, "journalist/profile-settings.html", context)


@login_required# Editors Views
def editor_dashboard_view(request):
    context={}
    context['page_title'] = 'Dashboard'
    return render(request, "editor/dashboard.html", context)

@login_required
def editor_article_list_view(request):
    context={}
    context['page_title'] = 'Article List'
    return render(request, "editor/article-list.html", context)

@login_required
def editor_current_article_view(request):
    context={}
    context['page_title'] = 'Article View'
    # If statemtn for usertype to go to current-article-2
    return render(request, "editor/current-article.html", context)

@login_required
def editor_reviews_view(request):
    context={}
    context['page_title'] = 'Reviews'
    return render(request, "editor/reviews.html", context)

@login_required
def editor_submitted_articles_view(request):
    context={}
    context['page_title'] = 'Article Feedback'
    return render(request, "editor/submitted-articles.html", context)

@login_required
def editor_messages_view(request):
    context={}
    context['page_title'] = 'Messages'
    return render(request, "editor/messages.html", context)

@login_required
def editor_notifications_view(request):
    context={}
    context['page_title'] = 'Notifications'
    return render(request, "editor/notifications.html", context)

@login_required
def editor_profile_view(request):
    context={}
    context['page_title'] = 'Profile Settings'
    return render(request, "editor/profile-settings.html", context)



@login_required# Director's Views
def director_dashboard_view(request):
    context={}
    context['page_title'] = 'Dashboard'
    return render(request, "director/dashboard.html", context)

@login_required
def director_article_list_view(request):
    context={}
    context['page_title'] = 'Tasks List'
    return render(request, "director/article-list.html", context)

@login_required
def director_current_article_view(request):
    context={}
    context['page_title'] = 'Task View'
    # If statemtn for usertype to go to current-article-2
    return render(request, "director/current-article.html", context)

@login_required
def director_reviews_view(request):
    context={}
    context['page_title'] = 'Reviews Statistics'
    return render(request, "director/reviews.html", context)

@login_required
def director_submitted_articles_view(request):
    context={}
    context['page_title'] = 'Task Feedback'
    return render(request, "director/submitted-articles.html", context)

@login_required
def director_messages_view(request):
    context={}
    context['page_title'] = 'Messages'
    return render(request, "director/messages.html", context)

@login_required
def director_notifications_view(request):
    context={}
    context['page_title'] = 'Notifications'
    return render(request, "director/notifications.html", context)

@login_required
def director_profile_view(request):
    context={}
    context['page_title'] = 'Profile Settings'
    return render(request, "director/profile-settings.html", context)




# Error pages
def handler400(request, exception):
    return render(request, 'error-pages/page-error-400.html', status=400)

def handler403(request, exception):
    return render(request, 'error-pages/page-error-403.html', status=403)

def handler404(request, exception):
    return render(request, 'error-pages/page-error-404.html', status=404)

def handler500(request):
    return render(request, 'error-pages/page-error-500.html', status=500)

def handler503(request):
    return render(request, 'error-pages/page-error-503.html', status=503)
