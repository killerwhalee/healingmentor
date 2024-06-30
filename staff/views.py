from django.shortcuts import render, redirect
from django.http import HttpResponse
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

    from urllib.parse import quote

    username = request.GET.get("username")

    if username is None:
        full_name = "all"
        gm_data = GuidedMeditation.objects.all()
        rg_data = RespiratoryGraph.objects.all()
        sa_data = SustainedAttention.objects.all()

    else:
        user = User.objects.get(username=username)
        full_name = user.profile.fullname
        gm_data = GuidedMeditation.objects.filter(user=user)
        rg_data = RespiratoryGraph.objects.filter(user=user)
        sa_data = SustainedAttention.objects.filter(user=user)

    session_data = {
        "Guided Meditation": gm_data.order_by("-date_created"),
        "Respiratory Graph": rg_data.order_by("-date_created"),
        "Sustained Attention": sa_data.order_by("-date_created"),
    }

    if request.method != "POST":
        context = {"session_data": session_data}
        return render(request, "staff/session.html", context)

    match request.POST["type"]:
        case "csv":
            import csv, codecs

            name = request.POST["session"]
            query_list = session_data.get(name)

            # Generate http response object
            response = HttpResponse(content_type="text/csv")
            response.write(codecs.BOM_UTF8)

            response["Content-Disposition"] = (
                f"attachment; filename=\"{name.replace(' ', '-')}_{quote(full_name)}.csv\""
            )

            # Create CSV writer
            writer = csv.writer(response)
            writer.writerow(
                [
                    "#",
                    "Class",
                    "Name",
                    "Date",
                    "How do you feel after meditation?",
                    "What sensations do you feel in your body?",
                    "Where, and how, do you feel your breathing?",
                    "How do you feel now, after writing this report?",
                ]
            )

            for query in query_list:
                pk = query.pk
                class_name = query.user.profile.classname
                full_name = query.user.profile.fullname
                date_created = query.date_created
                q = query.question
                q1, q2, q3, q4 = (
                    q.question_1,
                    q.question_2,
                    q.question_3,
                    q.question_4,
                )

                row = [pk, class_name, full_name, date_created, q1, q2, q3, q4]
                writer.writerow(row)

            return response

        case "graph":
            import io
            import random
            import pandas as pd
            import matplotlib.pyplot as plt

            name = request.POST["session"]
            query_list = session_data.get(name)

            datas = [
                (
                    f"#{query.id}",
                    pd.read_csv(query.csv_data.path, names=["time", "value"]),
                )
                for query in query_list
            ]

            plt.figure(figsize=(10, 5))
            plt.xlim(30, 60)
            plt.grid(True, linewidth=0.5)

            for _ in range(5):
                chart_id, data = random.choice(datas)
                plt.plot(
                    data["time"].values,
                    data["value"].values,
                    linewidth=4,
                    label=chart_id,
                )

            # Create buffer
            buf = io.BytesIO()
            plt.legend(loc="upper left", bbox_to_anchor=(0, -0.1), ncol=5)
            plt.savefig(buf, format="png")
            plt.close()

            buf.seek(0)

            # Generate http response object
            response = HttpResponse(buf, content_type="image/png")

            response["Content-Disposition"] = (
                f"attachment; filename=\"{name.replace(' ', '-')}_{quote(full_name)}.png\""
            )

            return response
