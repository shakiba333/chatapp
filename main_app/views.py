from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from django.db import models
from .models import Profile


def home(request):
    return render(request, 'home.html')


@login_required
def about(request):
    return render(request, 'about.html')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    profile_picture = forms.ImageField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            profile = Profile.objects.create(
                user=user,
                profile_picture=form.cleaned_data['profile_picture']
            )
            login(request, user)
            return redirect('profile')
        else:
            error_message = 'Invalid sign up - try again'
    else:
        form = SignUpForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def profile(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    context = {'user': user, 'profile': profile}
    return render(request, 'profile.html', context)
