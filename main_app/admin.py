from django.contrib import admin
from django.contrib.auth.models import User
from .models import ChatRoom, Profile
# Register your models here.

admin.site.register(Profile)

admin.site.register(ChatRoom)
