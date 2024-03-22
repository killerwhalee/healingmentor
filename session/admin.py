from django.contrib import admin
from session.models import (
    Multiplyer,
    Question,
    RespiratoryGraph,
    SustainedAttention,
    GuidedMeditation,
)

admin.site.register(Multiplyer)
admin.site.register(Question)
admin.site.register(RespiratoryGraph)
admin.site.register(SustainedAttention)
admin.site.register(GuidedMeditation)
