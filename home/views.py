from django.shortcuts import render

from board.models import Post


# Create your views here.
def index(request):
    notice_list = Post.objects.filter(category="notice").order_by("-date_created")[:5]

    context = {"notice_list": notice_list}
    return render(request, "home/index.html", context=context)

def contact_us(request):
    return render(request, "home/contact-us.html")