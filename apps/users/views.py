# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import *
from django.contrib import messages, sessions
import bcrypt

# Create your views here.
def greeting(request):
    return render(request, 'users/greeting.html')

def registration(request):
    # #First page where you enter email and password to register
    # if 'email' in request.POST and 'password' in request.POST:
    #     request.session['password'] = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
    #     request.session['email'] = request.POST['email']
    #     return render(request, 'users/userinfo.html')
    #Second page where you enter more info for the account
    # else:
    if 'fullname' in request.POST: # User is trying to register
        server_password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        user_name = request.POST['fullname']
        request.session['username'] = user_name
        user_email = request.POST['email']
        request.session['email'] = user_email
        new_user = User.objects.create(name=user_name, email=user_email, password=server_password, gender=request.POST['gender'], age=request.POST['age'])
        print('hitting here----------------------')
        print(request.POST)
        new_user.profile=request.FILES['profile_pic']
        new_user.save()
        # Registered user is automatically treated as logged in user, redirected to pin_index
        return redirect(reverse('pinterest:pin_index'))
    else: # User is trying to log in
        user_email = request.POST['email']
        if len(User.objects.filter(email=user_email)) < 1:
            tag = "no_user"
            error = "Invalid Username"
            messages.error(request, error, extra_tags=tag)
            return redirect(reverse("users:login"))
        else:
            visiting_user = User.objects.get(email=user_email)
            input_pw = request.POST["password"]
            if not bcrypt.checkpw(input_pw.encode('utf8'), visiting_user.password.encode('utf8')):
                tag = "password_incorrect"
                error = "Invalid Password"
                messages.error(request, error, extra_tags=tag)
                return redirect(reverse("users:login"))
            else:
                request.session["username"] = visiting_user.name
                request.session["email"] = visiting_user.email
                return redirect(reverse("pinterest:pin_index"))
def validate(request):
    message = "no error"
    errors = User.objects.validator(request.POST)

    if 'email_error' in errors or 'invalid_email' in errors:
        message = "email error"
    if 'password' in errors:
        message = 'password error'
    if 'name_error' in errors:
        message = 'name error'
    if 'age_error' in errors:
        message = 'age error'
    
    return HttpResponse(message)

def login(request):
    return render(request, 'users/login.html')
