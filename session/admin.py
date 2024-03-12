from django.contrib import admin
from .models import (
    Multiplyer,
    RespiratoryGraph,
    SustainedAttention,
    Question,
)

admin.site.register(Multiplyer)
admin.site.register(RespiratoryGraph)
admin.site.register(SustainedAttention)
admin.site.register(Question)
