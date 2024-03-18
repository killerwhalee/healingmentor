from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.paginator import Paginator

from _config.utils import uuid_filepath

from .forms import (
    RespiratoryGraphForm,
    SustainedAttentionForm,
    GuidedMeditationForm,
    QuestionForm,
)
from .models import (
    Multiplyer,
    RespiratoryGraph,
    SustainedAttention,
    GuidedMeditation,
    Question,
)


def calculate_score(user, time_input):
    # Import Multiplyer
    from django.core.exceptions import ObjectDoesNotExist

    try:
        mul_obj = Multiplyer.objects.get(user=user)
    except ObjectDoesNotExist:
        mul_obj = Multiplyer.objects.create(user=user)

    # Update Multiplyer date and amount
    from datetime import datetime, time, timedelta

    time_now = datetime.now()
    time_yesterday = time_now - timedelta(days=1)

    time_pivot_yd = datetime.combine(time_yesterday.date(), time(17, 0))
    time_pivot_am = datetime.combine(time_now.date(), time(5, 0))
    time_pivot_pm = datetime.combine(time_now.date(), time(17, 0))

    # Update daily multiplyer
    if time_now > time_pivot_pm and time_now != time_pivot_pm:
        mul_obj.daily_datetime = time_pivot_pm
        mul_obj.daily_tokens = 900
    elif time_now > time_pivot_am and time_now != time_pivot_am:
        mul_obj.daily_datetime = time_pivot_am
        mul_obj.daily_tokens = 900
    elif time_now != time_pivot_yd:
        mul_obj.daily_datetime = time_pivot_yd
        mul_obj.daily_tokens = 900

    # Update hourly multiplyer
    if time_now - mul_obj.hourly_datetime > timedelta(hours=1):
        mul_obj.hourly_datetime = time_now
        mul_obj.hourly_tokens = 300

    # Calculate multiplied score
    score = 0
    tokens_required = int(float(time_input))

    # Use hourly tokens
    tokens_used = min(tokens_required, mul_obj.hourly_tokens)
    score += tokens_used * (1 / 6) * 3
    tokens_required -= tokens_used
    mul_obj.hourly_tokens -= tokens_used

    # Use daily tokens
    tokens_used = min(tokens_required, mul_obj.daily_tokens)
    score += tokens_used * (1 / 6) * 3
    tokens_required -= tokens_used
    mul_obj.daily_tokens -= tokens_used

    # Add remainder
    score += tokens_required * (1 / 6)

    # Save multiplyer object
    mul_obj.save()

    # Return result score
    return score


def index(request):
    return render(request, "session/index.html")


@login_required(login_url="common:login")
def rg_record(request):
    if request.method == "POST":
        form_data = RespiratoryGraphForm(request.POST)
        form_question = QuestionForm(request.POST)

        if form_data.is_valid() and form_question.is_valid():
            # Create new question object
            q_obj = Question()

            q_obj.question_1 = form_question.cleaned_data["question_1"]
            q_obj.question_2 = form_question.cleaned_data["question_2"]
            q_obj.question_3 = form_question.cleaned_data["question_3"]
            q_obj.question_4 = form_question.cleaned_data["question_4"]

            q_obj.save()

            # Create new data object
            rg_obj = RespiratoryGraph()

            # Write user and time
            rg_obj.user = request.user
            rg_obj.date_created = timezone.now()

            # Write question data
            rg_obj.question = q_obj

            # Retrieve data from form
            csv_input = form_data.cleaned_data["csv_input"]
            time_input = form_data.cleaned_data["time_input"]

            # Write CSV data
            from urllib.parse import unquote

            file_path = uuid_filepath(rg_obj, "result.csv")
            rg_obj.csv_data.save(file_path, ContentFile(unquote(csv_input)))

            # Write score data
            rg_obj.score = calculate_score(request.user, time_input)

            # Save into model
            rg_obj.save()

            return redirect("session:rg-record")

    return render(request, "session/rg-record.html")


@login_required(login_url="common:login")
def rg_inquiry(request):
    # Initial variable settings
    data_list = []
    csv_x_data_list = []
    csv_y_data_list = []

    # Load all data if user is staff
    if request.user.is_staff:
        raw_data_list = RespiratoryGraph.objects.all().order_by("-date_created")
    # If not, load user data only
    else:
        raw_data_list = RespiratoryGraph.objects.filter(user=request.user).order_by(
            "-date_created"
        )

    # Paginate raw datas
    page = request.GET.get("page", 1)
    paginator = Paginator(raw_data_list, 10)
    raw_data_list = paginator.get_page(page)

    for data in raw_data_list:
        from _config.settings.base import MEDIA_ROOT
        import csv

        csv_x_data = []
        csv_y_data = []

        with open(f"{MEDIA_ROOT}/{data.csv_data}", "r") as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                csv_x_data.append(float(row[0]))
                csv_y_data.append(float(row[1]))

        csv_x_data_list.append(csv_x_data)
        csv_y_data_list.append(csv_y_data)

        data_list = zip(raw_data_list, csv_x_data_list, csv_y_data_list)

    # Send context to inquiry html template
    context = {
        "data_list": data_list,
        "page_obj": raw_data_list,
    }
    return render(request, "session/rg-inquiry.html", context)


@login_required(login_url="common:login")
def rg_delete(request, id):
    target_data = RespiratoryGraph.objects.get(id=id)

    # Process delete only if user matches
    if target_data.user == request.user:
        target_data.delete()
        return redirect("session:rg-inquiry")

    # Respond to (403)Forbidden if user does not match
    return HttpResponse(status=403)


@login_required(login_url="common:login")
def sa_record(request):
    if request.method == "POST":
        form_data = SustainedAttentionForm(request.POST)
        form_question = QuestionForm(request.POST)

        if form_data.is_valid() and form_question.is_valid():
            # Create new question object
            q_obj = Question()

            q_obj.question_1 = form_question.cleaned_data["question_1"]
            q_obj.question_2 = form_question.cleaned_data["question_2"]
            q_obj.question_3 = form_question.cleaned_data["question_3"]
            q_obj.question_4 = form_question.cleaned_data["question_4"]

            q_obj.save()

            # Create new data object
            sa_obj = SustainedAttention()

            # Write user and time
            sa_obj.user = request.user
            sa_obj.date_created = timezone.now()

            # Write question data
            sa_obj.question = q_obj

            # Retrieve data from form
            csv_input = form_data.cleaned_data["csv_input"]
            rate_input = form_data.cleaned_data["rate_input"]
            time_input = form_data.cleaned_data["time_input"]

            # Write CSV data
            from urllib.parse import unquote

            file_path = uuid_filepath(sa_obj, "result.csv")
            sa_obj.csv_data.save(file_path, ContentFile(unquote(csv_input)))

            # Write rate data
            sa_obj.rate_data = rate_input

            # Write score data
            sa_obj.score = calculate_score(request.user, time_input)

            # Save into model
            sa_obj.save()

            return redirect("session:sa-record")

    return render(request, "session/sa-record.html")


@login_required(login_url="common:login")
def sa_inquiry(request):
    # Initial variable settings
    data_list = []
    csv_x_data_list = []
    csv_y_data_list = []

    # Load all data if user is staff
    if request.user.is_staff:
        raw_data_list = SustainedAttention.objects.all().order_by("-date_created")
    # If not, load user data only
    else:
        raw_data_list = SustainedAttention.objects.filter(user=request.user).order_by(
            "-date_created"
        )

    # Paginate raw datas
    page = request.GET.get("page", 1)
    paginator = Paginator(raw_data_list, 10)
    raw_data_list = paginator.get_page(page)

    for data in raw_data_list:
        from _config.settings.base import MEDIA_ROOT
        import csv

        csv_x_data = []
        csv_y_data = []

        with open(f"{MEDIA_ROOT}/{data.csv_data}", "r") as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                csv_x_data.append(float(row[0]))
                csv_y_data.append(float(row[1]))

        csv_x_data_list.append(csv_x_data)
        csv_y_data_list.append(csv_y_data)

        data_list = zip(raw_data_list, csv_x_data_list, csv_y_data_list)

    # Send context to inquiry html template
    context = {
        "data_list": data_list,
        "page_obj": raw_data_list,
    }
    return render(request, "session/sa-inquiry.html", context)


@login_required(login_url="common:login")
def sa_delete(request, id):
    target_data = SustainedAttention.objects.get(id=id)

    # Process delete only if user matches
    if target_data.user == request.user:
        target_data.delete()
        return redirect("session:sa-inquiry")

    # Respond to (403)Forbidden if user does not match
    return HttpResponse(status=403)


@login_required(login_url="common:login")
def gm_record(request):
    if request.method == "POST":
        form_data = GuidedMeditationForm(request.POST)
        form_question = QuestionForm(request.POST)

        if form_data.is_valid() and form_question.is_valid():
            # Create new question object
            q_obj = Question()

            q_obj.question_1 = form_question.cleaned_data["question_1"]
            q_obj.question_2 = form_question.cleaned_data["question_2"]
            q_obj.question_3 = form_question.cleaned_data["question_3"]
            q_obj.question_4 = form_question.cleaned_data["question_4"]

            q_obj.save()

            # Create new data object
            gm_obj = GuidedMeditation()

            # Write user and time
            gm_obj.user = request.user
            gm_obj.date_created = timezone.now()

            # Write question data
            gm_obj.question = q_obj

            # Write lecture data
            lecture_input = form_data.cleaned_data["lecture_input"]
            gm_obj.lecture = lecture_input

            # Write score data
            gm_obj.score = 5

            # Save into model
            gm_obj.save()

            return redirect("session:gm-record")

    return render(request, "session/gm-record.html")
