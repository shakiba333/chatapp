from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('users/', views.user_list, name='user_list'),
    path('chat_room/<str:other_username>/', views.chat_room, name='chat_room'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
