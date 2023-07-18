from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import (
    UserCreationForm, 
    UserChangeForm, 
    PasswordChangeForm
    )
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from django.db import models
from .models import Profile
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import ChatRoom


def home(request):
    return render(request, 'home.html')


@login_required
def about(request):
    return render(request, 'about.html')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=250)
    last_name = forms.CharField(max_length=250)
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

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            profile_picture = form.cleaned_data['profile_picture']
            if profile_picture:
                request.user.profile.profile_picture = profile_picture
                request.user.profile.save()
            form.save()
            return redirect('profile')

    else:
        form = EditProfileForm(instance=request.user)
    args = {'form':form}
    return render(request, 'edit_profile.html', args)


class EditProfileForm(UserChangeForm):
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = (
            'username',
            'email', 
            'first_name', 
            'last_name',
        )

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')
        else:
            return redirect('change-password')
    
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'change_password.html', args)


class DeleteUser(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'delete_user_confirm.html'
    success_message = "User has been deleted"
    success_url = reverse_lazy('home')

@login_required
def user_list(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'user_list.html', context)


@login_required
def chat_room(request, other_username):
    user = request.user
    other_username = User.objects.get(username=other_username)
    if request.method == 'POST':
        message = request.POST['message']
        chat_room = ChatRoom.objects.create(
            user=user, other_user=other_username, message=message)
    chat_rooms = ChatRoom.objects.filter(user=user, other_user=other_username) | ChatRoom.objects.filter(
        user=other_username, other_user=user)
    context = {'user': user, 'other_user': other_username,
               'chat_rooms': chat_rooms}
    return render(request, 'chat_room.html', context)

