from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from .models import Employee, Profile, CapacityChoices, Journalist, Editor, Director
from django.utils.text import slugify

# Create your views here.

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
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
            return super().get_success_url()  # Fallback to the default success URL

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
    view_messages = []
    context['username'] = ''
    if(request.method == 'POST'):
        
        email = request.POST.get('email')
        id_card_number = request.POST.get('id_card_number')
        password = request.POST.get('password1')
        confirm_passord = request.POST.get('password2')

        # Check if user exists
        # create profile if it does not exist
        # add to appropriate employee table if it does not exist
        user = User.objects.filter(email=email).first()
        if (user and Profile.objects.filter(user=user, id_card_number=id_card_number)):
            errors.append("Account exists. Go to Login page to login")
            context['errors'] = errors
            return render(request, "users/register.html", context)

        if (not(password==confirm_passord)):
            errors.append("Make sure the passwords match")
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
            print("Employee Does not exist")
            return render(request, "users/register.html", context)
        
        if (employee):
            # create username
            
            username = employee.id_card_number

            # create user
            user = User(username=username, email=email, first_name=employee.first_name, last_name=employee.other_names)
            user.set_password(password)
            user.save()

            # create user profile
            user_profile = Profile(user=user, email=email, id_card_number=id_card_number, capacity=employee.capacity)
            user_profile.save()

            capacity = employee.capacity

            if capacity == CapacityChoices.WRITER:
                # insert in journalist table
                journalist_user = Journalist(user=user, type=capacity)
                journalist_user.save()
            elif capacity == CapacityChoices.PHOTOJOURNALIST:
                # insert in journalist table
                journalist_user = Journalist(user=user, type=capacity)
                journalist_user.save()
            elif capacity == CapacityChoices.EDITOR:
                # insert in journalist table
                editor_user = Editor(user=user)
                editor_user.save()
            elif capacity == CapacityChoices.DIRECTOR:
                # insert in journalist table
                director_user = Director(user=user)
                director_user.save()
            
            messages.success(request, f'{username}', extra_tags='username')
            messages.success(request, f'Account Created Successfully. Now you can login with your id number: {username}.', extra_tags='alert_message')
            return redirect('login')
        
        else:
            errors.append("Employee Record doesn't exists. Recheck ID card number and Email details.")
            context['errors'] = errors
            return render(request, "users/register.html", context)    


    
    return render(request, "users/register.html", context)

# def login_redirector(request):
#     user_type = request.user.profile.user_type


