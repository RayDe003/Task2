from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import ViewRequests

urlpatterns = [
    path('', ViewRequests.as_view(), name='index'),
    path('register/', views.registration, name='register'),
    path('home/', views.home, name='home'),
    path('login/', views.login_v, name='login'),
    path('logout/', views.logout_view, name='logout'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)