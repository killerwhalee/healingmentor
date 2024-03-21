from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from django.shortcuts import render
from .forms import RegisterForm


# Views for User Authentication
def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            # Save User Data
            form.save()

            # Authenticate User
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            login(request, user)
            return render(request, "common/signup-success.html")
    else:
        form = RegisterForm()

    context = {"form": form}
    return render(request, "common/signup.html", context)


def terms(request):
    return render(request, "common/terms.html")


def profile(request, username):
    user = User.objects.get(username=username)
    context = {"user": user}
    return render(request, "common/profile.html", context)


# Views for Downloading Media
def download(request, path):
    from _config.settings.base import MEDIA_ROOT
    import os

    file_path = os.path.join(MEDIA_ROOT, path)

    if os.path.exists(file_path):
        file_ext = os.path.splitext(file_path)[-1]

        with open(file_path, "r", encoding="UTF-8") as file:
            response = HttpResponse(file.read())
            response[
                "Content-Disposition"
            ] = f'attachment; filename="download{file_ext}"'
            return response


# Views for Error Handling
def error400(request, exception):
    return render(request, "error/400.html", {})


def error403(request, exception):
    return render(request, "error/403.html", {})


def error404(request, exception):
    return render(request, "error/404.html", {})


def error500(request):
    return render(request, "error/500.html", {})


def error502(request):
    return render(request, "error/502.html", {})


def error503(request):
    return render(request, "error/503.html", {})
