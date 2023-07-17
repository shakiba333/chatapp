from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='upload/')

    def __str__(self):
        return self.user.username


class ChatRoom(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='chat_rooms_as_user')
    other_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='chat_rooms_as_other_user')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
