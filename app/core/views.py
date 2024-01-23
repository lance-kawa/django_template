from django.conf import settings
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from api.models import User
from django.utils.translation import activate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def change_language(request, lang_code):
    activate(lang_code)
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response

def home(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html", {})

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, "dashboard/index.html", {
        'user': request.user,
    })