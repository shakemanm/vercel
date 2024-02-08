from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('', views.Home, name='home'),
    path('register/', views.Register, name='register'),
    path('otp/<str:phone_number>/', views.Otp, name='otp')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)