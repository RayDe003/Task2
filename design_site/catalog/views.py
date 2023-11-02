from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import ListView
from django.utils import timezone
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from .models import Request


# Create your views here.
def index(request):
    return render (request, 'index.html')
    # requests_list = Request.objects.all()
    # return render(request, 'index.html', {'requests_list': requests_list})

def home(request):
    return render(request, 'home.html')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            fio = form.cleaned_data['fio']

            user = form.save()
            user.first_name = fio
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_v(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error_message('Неправильный логин или пароль.')
        else:
            form.add_error_message('Пожалуйста, исправьте ошибки в форме.')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

# class RequestsView(generic.ListView):
#     model = Request
#     paginate_by = 4



# def requestView(generic.ListView):
#     requests_list = Request.objects.all()  # Получение всех заявок
#     return render(request, 'index.html', {'requests_list': requests_list})

def logout_view(request):
    logout(request)  # Выход пользователя
    return redirect('index')

class ViewRequests(ListView):
   model = Request
   template_name = 'index.html'
   context_object_name = 'requests'
   completed_requests = Request.objects.filter(is_completed=True).order_by('-date_create','-time_create')[:4]

