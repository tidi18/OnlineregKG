from django.http import HttpResponse
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.views import LogoutView
from .models import Profile


def check_blocked(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            if profile.is_blocked:
                return HttpResponse('Вы заблокированы. Пожалуйста, свяжитесь с администратором. Отправьте сообщение в разделе контакты!')

        return view_func(request, *args, **kwargs)
    return wrapper


class BlockedUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            if profile.is_blocked:
                return HttpResponse('Вы заблокированы. Пожалуйста, свяжитесь с администратором. Отправьте сообщение в разделе контакты!')
        return super().dispatch(request, *args, **kwargs)


class UserRegisterView(BlockedUserMixin, SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'users/registration.html'
    success_message = 'Вы успешно зарегистрировались. Можете войти на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.save()
        return response


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/entrance.html'
    next_page = 'index'
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context


class UserLogoutView(LogoutView):
    next_page = 'index'



