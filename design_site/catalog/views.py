from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .forms import RegistrationForm, LoginForm, RequestForm
from django.contrib.auth import login, authenticate, logout

from .models import Request


# Create your views here.
def index(request):
    return render (request, 'index.html')

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

def logout_view(request):
    logout(request)
    return redirect('index')

class ViewRequests(ListView):
   model = Request
   template_name = 'index.html'
   context_object_name = 'requests'

class RequestCreate(LoginRequiredMixin, CreateView):
    model = Request
    form_class = RequestForm
    template_name = 'auth_user/request_form.html'
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def user_requests(request):
        user = request.user
        requests = Request.objects.filter(user=user)
        return render(request, 'auth_user/my_requests.html', {'requests': requests})


def delete_request(request, request_id):
    user = request.user
    request_to_delete = get_object_or_404(Request, id=request_id, user=user)

    if request.method == 'POST':
        request_to_delete.delete()
        return redirect('home')

    return render(request, 'auth_user/delete_request.html', {'request_to_delete': request_to_delete})
