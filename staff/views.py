from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required(login_url="common:login")
def index(request):
    return render(request, "staff/index.html")


@staff_member_required(login_url="common:login")
def user(request):
    from common.models import User

    user_list = User.objects.all()

    user_data = {}

    for user in user_list:
        classname = user.profile.classname

        if classname not in user_data:
            user_data[classname] = []

        user_data[classname].append(user)

    user_data_sorted = {k: user_data[k] for k in sorted(user_data.keys())}
    context = {"user_data": user_data_sorted}
    return render(request, "staff/user.html", context)


@staff_member_required(login_url="common:login")
def session(request):
    from common.models import User
    from session.models import (
        GuidedMeditation,
        RespiratoryGraph,
        SustainedAttention,
    )

    username = request.GET.get("username")
    
    if username is None:
        gm_data = GuidedMeditation.objects.all()
        rg_data = RespiratoryGraph.objects.all()
        sa_data = SustainedAttention.objects.all()
        
    else:
        user = User.objects.get(username=username)
        gm_data = GuidedMeditation.objects.filter(user=user)
        rg_data = RespiratoryGraph.objects.filter(user=user)
        sa_data = SustainedAttention.objects.filter(user=user)

    session_data = {
        "Guided Meditation": gm_data.order_by("-date_created"),
        "Respiratory Graph": rg_data.order_by("-date_created"),
        "Sustained Attention": sa_data.order_by("-date_created"),
    }

    context = {"session_data": session_data}
    return render(request, "staff/session.html", context)
