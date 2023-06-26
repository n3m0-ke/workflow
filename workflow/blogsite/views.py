from django.shortcuts import render

# Create your views here.

def blog_home_view(request):
    context={}
    return render(request, "blogsite/index.html", context)

def blog_view(request):
    context={}
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
