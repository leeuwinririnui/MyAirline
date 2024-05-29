from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser

def login_view(request):
    if request.method == 'POST':

        # retrieve email
        username = request.POST.get('username', None)
        # retrieve password
        password = request.POST.get('password', None)

        # authenticate user
        user = authenticate(username=username, password=password)
        # if user exists, log user in and redirect to home page
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        # access POST data

        # retrieve username
        username = request.POST.get('username', None)
        # retrieve first name
        first_name = request.POST.get('first_name', None)
        # retrieve last name
        last_name = request.POST.get('last_name', None)
        # retrieve gender
        gender = request.POST.get('gender', None)
        # retrieve title
        title = request.POST.get('title', None)
        # retrieve email
        email = request.POST.get('email', None)
        # retrieve password
        password = request.POST.get('password', None)
        # retrieve password confirmation
        confirm = request.POST.get('confirm', None)

        error_messages = []
        
        # check to see if user with provided email already exists
        if CustomUser.objects.filter(email=email).exists():
            error_messages.append("A user with this email already exists.")

        if len(email) < 4:
            error_messages.append("Email must be at least 4 characters long.")

        if password != confirm:
            error_messages.append("Passwords do not match.")

        if len(password) < 7:
            error_messages.append("Password must have 7 or more characters.")
        
        # if error return error message
        if error_messages:
            return render(request, 'signup.html', {'error_messages': error_messages})
        else:
            # process data and save to database

            # hash the password
            hashed_password = make_password(password)

            # create new User instance
            new_user = CustomUser(username=username,
                            first_name=first_name, 
                            last_name=last_name, 
                            email=email,
                            gender=gender,
                            title=title, 
                            password=hashed_password)

            # save new user to database
            new_user.save()

            # authenticate new user
            user = authenticate(username=username, password=password)

            login(request, user)

            # redirect to the home page after successful signup
            return redirect('home')

    return render(request, 'signup.html')

def logout_view(request): 
    if request.method == 'POST':
        # log user out
        logout(request)
        # return user to loging screen
        return redirect('login')
    return render(request, 'logout.html')