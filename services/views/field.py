from django.shortcuts import render
from services.models import Service


def service_field(request, field):
    field_name = field.replace('-', ' ').title()
    services = Service.objects.filter(field=field_name).order_by("-date")
    return render(request, 'services/field.html', {'services': services, 'field': field_name})
