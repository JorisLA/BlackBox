from django.shortcuts import render
from django.http import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

from app.models import Team, Player


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = UserCreationForm()
    return render(request, 'authentification/signup.html', {'form': form})

class LoginView(TemplateView):

  template_name = 'authentification/index.html'

  def post(self, request, **kwargs):

    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    return render(request, self.template_name)

class LogoutView(TemplateView):

  template_name = 'authentification/index.html'

  def get(self, request, **kwargs):

    logout(request)

    return render(request, self.template_name)
