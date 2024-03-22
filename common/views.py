from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from common.forms import RegisterForm, ProfileForm


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


@login_required(login_url="common:login")
def profile(request):
    form = ProfileForm()
    
    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,
        )

        if form.is_valid():
            form.save()
            return redirect("common:profile")

    context = {"user": request.user, "form": form}
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
            response["Content-Disposition"] = (
                f'attachment; filename="download{file_ext}"'
            )
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
