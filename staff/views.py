from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from common.models import User


@staff_member_required(login_url="common:login")
def index(request):
    return render(request, "staff/index.html")


@staff_member_required(login_url="common:login")
def user(request):
    user_list = User.objects.all()

    user_data = {}

    for user in user_list:
        classname = user.profile.classname

        if classname not in user_data:
            user_data[classname] = []

        user_data[classname].append(user)
    
    print(user_data)

    context = {"user_data": user_data}
    return render(request, "staff/user.html", context)
