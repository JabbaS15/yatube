from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class ChangePassword(PasswordChangeView):
    success_url = reverse_lazy('users:password_change')
    template_name = 'users/password_reset_done.html'
