from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import ViewRequests, RequestCreate

urlpatterns = [
    path('', ViewRequests.as_view(), name='index'),
    path('register/', views.registration, name='register'),
    path('home/', views.home, name='home'),
    path('login/', views.login_v, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('request_form/', RequestCreate.as_view(), name='request_form'),
    path('my_requests/', views.user_requests, name='user_requests'),
    path('delete_request/<int:request_id>/', views.delete_request, name='delete_request'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
