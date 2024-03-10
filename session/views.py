from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.paginator import Paginator

from _config.utils import uuid_filepath

from .forms import RespiratoryGraphForm, SustainedAttentionForm
from .models import MultiplyerData, RespiratoryGraphData, SustainedAttentionData


def calculate_score(user, time_input):
    # Import MultiplyerData
    from django.core.exceptions import ObjectDoesNotExist

    try:
        mul_obj = MultiplyerData.objects.get(user=user)
    except ObjectDoesNotExist:
        mul_obj = MultiplyerData.objects.create(user=user)

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
        form = RespiratoryGraphForm(request.POST)

        if form.is_valid():
            # Create new data object
            rg_obj = RespiratoryGraphData()

            # Write user and time
            rg_obj.user = request.user
            rg_obj.date_created = timezone.now()

            # Retrieve data from form
            csv_input = form.cleaned_data["csv_input"]
            time_input = form.cleaned_data["time_input"]
            note_input = form.cleaned_data["note_input"]

            # Write CSV data
            from urllib.parse import unquote

            file_path = uuid_filepath(rg_obj, "result.csv")
            rg_obj.csv_data.save(file_path, ContentFile(unquote(csv_input)))

            # Write score data
            rg_obj.score = calculate_score(request.user, time_input)

            # Write note data
            rg_obj.note = note_input

            # Save into model
            rg_obj.save()

            return redirect("session:rg-record")

    form = RespiratoryGraphForm()
    context = {"form": form}
    return render(request, "session/rg-record.html", context)


@login_required(login_url="common:login")
def rg_inquiry(request):
    # Initial variable settings
    data_list = []
    csv_x_data_list = []
    csv_y_data_list = []

    # Load all data if user is staff
    if request.user.is_staff:
        raw_data_list = RespiratoryGraphData.objects.all().order_by("-date_created")
    # If not, load user data only
    else:
        raw_data_list = RespiratoryGraphData.objects.filter(user=request.user).order_by(
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
    target_data = RespiratoryGraphData.objects.get(id=id)

    # Process delete only if user matches
    if target_data.user == request.user:
        target_data.delete()
        return redirect("session:rg-inquiry", request.user)

    # Respond to (403)Forbidden if user does not match
    return HttpResponse(status=403)


@login_required(login_url="common:login")
def sa_record(request):
    if request.method == "POST":
        form = SustainedAttentionForm(request.POST)

        if form.is_valid():
            # Create new data object
            sa_obj = SustainedAttentionData()

            # Write user and time
            sa_obj.user = request.user
            sa_obj.date_created = timezone.now()

            # Retrieve data from form
            csv_input = form.cleaned_data["csv_input"]
            rate_input = form.cleaned_data["rate_input"]
            time_input = form.cleaned_data["time_input"]
            note_input = form.cleaned_data["note_input"]

            # Write CSV data
            from urllib.parse import unquote

            file_path = uuid_filepath(sa_obj, "result.csv")
            sa_obj.csv_data.save(file_path, ContentFile(unquote(csv_input)))

            # Write rate data
            sa_obj.rate_data = rate_input

            # Write score data
            sa_obj.score = calculate_score(request.user, time_input)

            # Write note data
            sa_obj.note = note_input

            # Save into model
            sa_obj.save()

            return redirect("session:sa-record")

    form = SustainedAttentionForm()
    context = {"form": form}
    return render(request, "session/sa-record.html", context)


@login_required(login_url="common:login")

def sa_inquiry(request):
    # Initial variable settings
    data_list = []
    csv_x_data_list = []
    csv_y_data_list = []

    # Load all data if user is staff
    if request.user.is_staff:
        raw_data_list = RespiratoryGraphData.objects.all().order_by("-date_created")
    # If not, load user data only
    else:
        raw_data_list = RespiratoryGraphData.objects.filter(user=request.user).order_by(
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
    target_data = SustainedAttentionData.objects.get(id=id)

    # Process delete only if user matches
    if target_data.user == request.user:
        target_data.delete()
        return redirect("session:sa-inquiry", request.user)

    # Respond to (403)Forbidden if user does not match
    return HttpResponse(status=403)


@login_required(login_url="common:login")
def gm_record(request):
    if request.method == "POST":
        form = SustainedAttentionForm(request.POST)

        if form.is_valid():
            # Create new data object
            sa_obj = SustainedAttentionData()

            # Write user and time
            sa_obj.user = request.user
            sa_obj.date_created = timezone.now()

            # Retrieve data from form
            csv_input = form.cleaned_data["csv_input"]
            rate_input = form.cleaned_data["rate_input"]
            time_input = form.cleaned_data["time_input"]
            note_input = form.cleaned_data["note_input"]

            # Write CSV data
            from urllib.parse import unquote

            file_path = uuid_filepath(sa_obj, "result.csv")
            sa_obj.csv_data.save(file_path, ContentFile(unquote(csv_input)))

            # Write rate data
            sa_obj.rate_data = rate_input

            # Write score data
            sa_obj.score = calculate_score(request.user, time_input)

            # Write note data
            sa_obj.note = note_input

            # Save into model
            sa_obj.save()

            return redirect("session:gm-record")

    form = SustainedAttentionForm()
    context = {"form": form}
    return render(request, "session/gm-record.html", context)
