from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
    path('profile/<int:pk>/delete/', views.ProfileDelete.as_view(), name='profile_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
