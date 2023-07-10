from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.utils import timezone

from django.db.models import Count, Q
from pages.models import Task, PhotoGallery, TaskStatusChoices, Reviews, Category, Tags, Click
from .models import UserContactMessage
from users.models import CapacityChoices

# Create your views here.

def blog_home_view(request):
    
    context={}
    all_posts = Task.objects.all().order_by('-publication_date')
    main_posts = Task.objects.all().order_by('-publication_date')[:3]
    side_posts = Task.objects.all().order_by('-publication_date')[:5]
    categories = Category.objects.all()
    top_tags = Tags.objects.annotate(num_tasks=Count('tags')).order_by('-num_tasks')[:10]
    top_ten_tags = Tags.objects.all()[:10]
    context['tope_ten_tags'] = top_ten_tags
    context['top_tags'] = top_tags
    context['categories'] = categories
    context['all_posts'] = all_posts
    context['main_posts'] = main_posts
    context['side_posts'] = side_posts
    return render(request, "blogsite/index.html", context)

def blog_preview(request, task_id):

    user = request.user

    if (user.profile.capacity != CapacityChoices.DIRECTOR) and (user.profile.capacity != CapacityChoices.EDITOR) and (user.profile.capacity != CapacityChoices.PHOTOJOURNALIST) and (user.profile.capacity != CapacityChoices.WRITER):

        raise Http404('Page not found')
    else:
        task = Task.objects.get(id=task_id)
        if not(task) or task.status != 'approved':
            messages.error(request, 'This Blog Article is not available for viewing')
            return redirect('blog-home')

        context={}

        top_tags = Tags.objects.annotate(num_tasks=Count('tags')).order_by('-num_tasks')[:10]
        top_ten_tags = Tags.objects.all()[:10]
        context['tope_ten_tags'] = top_ten_tags
        context['top_tags'] = top_tags
        all_posts = Task.objects.all().order_by('-publication_date')
        context['all_posts'] = all_posts
        categories = Category.objects.all()
        context['categories'] = categories

        article = task.article
        context['task'] = task
        context['article'] = article

        sections = article.article_sections.all()
        context['sections'] = sections

        photo_gallery = PhotoGallery.objects.filter(article=article).first()
        context['photo_gallery'] = photo_gallery

        journalists = []

        if(photo_gallery):
            photo_gallery_journalist = photo_gallery.journalist
            journalists.append(photo_gallery_journalist)

        images = photo_gallery.images.all()
        context['images'] = images

        if sections:
            for section in sections:
                section_journalist = section.journalist
                journalists.append(section_journalist)
        
        context['journalists'] = journalists

        if images:
            image1 = images.filter(name='one').first()
            context['image1'] = image1
            image2 = images.filter(name='two').first()
            context['image2'] = image2
            image3 = images.filter(name='three').first()
            context['image3'] = image3
        
        print(task.publication_date)

        context['other_posts'] = Task.objects.filter(status=TaskStatusChoices.APPROVED).exclude(id=task.id)    
        
        return render(request, "blogsite/blog-preview.html", context)

def blog_view(request, task_id):

    task = Task.objects.get(id=task_id)
    if not(task) or task.status != 'approved':
        messages.error(request, 'This Blog Article is not available for viewing')
        return redirect('blog-home')

    context={}

    task.click_count += 1
    task.save()

    click = Click(task=task, date=timezone.now().date())
    click.save()

    categories = Category.objects.all()
    context['categories'] = categories
    all_posts = Task.objects.all().order_by('-publication_date')
    context['all_posts'] = all_posts
    top_tags = Tags.objects.annotate(num_tasks=Count('tags')).order_by('-num_tasks')[:10]
    top_ten_tags = Tags.objects.all()[:10]
    context['tope_ten_tags'] = top_ten_tags
    context['top_tags'] = top_tags

    if(request.method=='POST'):
        if(request.POST.get('name')):
            name = request.POST.get('name')
        else:
            name = 'anonymous user'
        
        if(request.POST.get('email')):
            email = request.POST.get('email')
        else:
            email = ''
        
        if(request.POST.get('rating')):
            rating = request.POST.get('rating')
        else:
            rating = ''
        
        review = request.POST.get('message')

        for key, value in request.POST.items():
            print(f'{key}: {value}')

        new_review = Reviews(task=task, name=name, email=email, review=review, rating=rating, review_date=timezone.now())
        new_review.save()

        review_message = ''
        review_message+="Review Saved successfully"
        context['review_message'] = review_message

    article = task.article
    context['task'] = task
    context['article'] = article

    sections = article.article_sections.all()
    context['sections'] = sections

    photo_gallery = PhotoGallery.objects.filter(article=article).first()
    context['photo_gallery'] = photo_gallery

    journalists = []

    if(photo_gallery):
        photo_gallery_journalist = photo_gallery.journalist
        journalists.append(photo_gallery_journalist)

    images = photo_gallery.images.all()
    context['images'] = images

    if sections:
        for section in sections:
            section_journalist = section.journalist
            journalists.append(section_journalist)
    
    context['journalists'] = journalists

    if images:
        image1 = images.filter(name='one').first()
        context['image1'] = image1
        image2 = images.filter(name='two').first()
        context['image2'] = image2
        image3 = images.filter(name='three').first()
        context['image3'] = image3
    
    print(task.publication_date)

    context['other_posts'] = Task.objects.filter(status=TaskStatusChoices.APPROVED).exclude(id=task.id)    
    
    return render(request, "blogsite/post-details.html", context)

def blog_list_view(request):
    context={}
    category_name = request.GET.get('category')
    tag_name = request.GET.get('tag')
    search_query = request.GET.get('search_query')

    posts = Task.objects.all()

    if category_name:
        posts = posts.filter(categories__category_name__iexact=category_name)
        search_term=category_name+' blogs'
        context['search_term'] = search_term

    if tag_name:
        posts = posts.filter(tags__tag_name__iexact=tag_name)
        search_term=tag_name+' blogs'
        context['search_term'] = search_term

    if search_query:
        posts = posts.filter(
            Q(article__title__icontains=search_query) |
            Q(article__subtext__icontains=search_query) |
            Q(categories__category_name__icontains=search_query) |
            Q(tags__tag_name__icontains=search_query)
        )
        search_term=search_query+' blogs'
        context['search_term'] = search_term
    
    all_posts = Task.objects.all().order_by('-publication_date')

    context['all_posts'] = all_posts
    
    context['posts'] = posts.order_by('-publication_date')

    return render(request, "blogsite/blog-list.html", context)

def contact_us_view(request):
    
    context={}
    
    if(request.method=='POST'):
        if(request.POST.get('name')):
            name = request.POST.get('name')
        else:
            name = 'anonymous user'
        
        if(request.POST.get('email')):
            email = request.POST.get('email')
        else:
            email = ''
        
        if(request.POST.get('subject')):
            subject = request.POST.get('subject')
        else:
            subject = ''
        
        message = request.POST.get('message')

        user_message_contact = UserContactMessage(name=name, email=email, message=message, subject=subject, message_time=timezone.now())
        user_message_contact.save()

        success_message = ''
        success_message +="Message Sent successfully"
        context['success_message'] = success_message


    return render(request, "blogsite/contact.html", context)

def about_us_view(request):
    context={}
    return render(request, "blogsite/about.html", context)
