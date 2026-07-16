from django.shortcuts import render
from services.models import Service


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})
