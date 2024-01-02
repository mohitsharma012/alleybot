from django.shortcuts import render,redirect
from userauth.models import users
from allybot.views import index
from dashboard.views import *


# function to register new user 
def user_registration(request):
    if request.method == 'POST':
        # get data from form 
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        user_pass = request.POST.get('user_pass')
        user_cpass = request.POST.get('user_cpass')
        # checking password and Confirm Password match 
        if (user_pass ==user_cpass):
            # check user is in database or not 
            check_user = users.objects.filter(user_email=user_email)
            if len(check_user)==0:
                new_user = users(user_name=user_name,user_email=user_email,user_pass=user_pass)
                new_user.save()
                print("user registered")
            else:
                print("email already registered")
        else:
            print("Password Did not match")
    return redirect(index)

# function to login user
def user_login(request):
    if request.method == 'POST':
        # get data from form 
        user_email = request.POST.get('user_email')
        user_pass = request.POST.get('user_pass')
        # get data from database to check login details 
        if users.objects.filter(user_email=user_email).exists():
            data_email = users.objects.get(user_email=user_email)
        
            if user_pass == data_email.user_pass :
                request.session['user_id'] = data_email.user_id  # Store user_id in session
                return redirect(dashboard)
            else:
                print("email id or password did't match")
                return redirect(index)
        else:
            print("no user found ")
            return redirect(index)

# this is an logout function 
def user_logout(request):
    request.session.flush()  # Clear the session
    return redirect(index)

