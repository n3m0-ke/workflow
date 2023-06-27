from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Employee, Profile
from django.utils.text import slugify

# Create your views here.

def generate_unique_username(first_name, other_names):
    # Combine first_name and other_names
    full_name = f"{first_name} {other_names}"

    # Create a slug from the full name
    slug = slugify(full_name)

    # Check if the slug is already used as a username
    count = User.objects.filter(username__startswith=slug).count()

    # Append a unique number to the slug if it's already taken
    if count > 0:
        username = f"{slug}{count + 1}"
    else:
        username = slug

    return username

def registration_view(request):
    context={}
    errors = []
    messages = []
    if(request.method == 'POST'):
        username = request.POST.get('username')
        email = request.POST.get('email')
        id_card_number = request.POST.get('id_card_number')
        password = request.POST.get('password1')
        confirm_passord = request.POST.get('password2')

        if (not(password==confirm_passord)):
            errors.append("Make sure the passords match")
            context['errors'] = errors
            return render(request, "users/register.html", context)
        
        # Check if the user exists in the employees table
        try:
            # employee = Employee.objects.get(id_card_number=id_card_number)
            employee = Employee.objects.filter(id_card_number=id_card_number, email=email).first()

        except Employee.DoesNotExist:
            # User does not exist in the employees table
            # Handle the error or redirect to an appropriate page
            errors.append("Failed to register. Unknown credentials")
            context['errors'] = errors
            return render(request, "users/register.html", context)
        
        # create username
        if not username:
            username = generate_unique_username(employee.first_name, employee.other_names)
        else:
            count = User.objects.filter(username__startswith=username).count()
            if count > 0:
                username = f"{username}{count + 1}"
            else:
                username = username

        # create user
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        # create user profile
        user_profile = Profile(user=user, email=email, id_card_number=id_card_number, capacity=employee.capacity)
        user_profile.save()

        messages.append("Account Created Successfully. Now you can login.")
        context['messages'] = messages

        return render(request, "users/login.html", context)


    
    return render(request, "users/register.html", context)

# def login_redirector(request):
#     user_type = request.user.profile.user_type


