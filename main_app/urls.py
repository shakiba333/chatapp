from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete_user/<int:pk>/', views.DeleteUser.as_view(), name='delete_user'),
    path('users/', views.user_list, name='user_list'),
    path('chat_room/<str:other_username>/', views.chat_room, name='chat_room'),
    path('chat_history/', views.chat_history, name='chat_history'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
