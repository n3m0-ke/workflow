from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from pages.models import Task, PhotoGallery, TaskStatusChoices
from users.models import CapacityChoices

# Create your views here.

def blog_home_view(request):
    
    context={}
    all_posts = Task.objects.all().order_by('-publication_date')
    main_posts = Task.objects.all().order_by('-publication_date')[:3]
    side_posts = Task.objects.all().order_by('-publication_date')[:5]
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
    return render(request, "blogsite/blog.html", context)

def contact_us_view(request):
    context={}
    return render(request, "blogsite/contact.html", context)

def about_us_view(request):
    context={}
    return render(request, "blogsite/about.html", context)
