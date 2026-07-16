from django.shortcuts import render, get_object_or_404
from services.models import Service


def index(request, id):
    service = get_object_or_404(Service, id=id)
    return render(request, 'services/single_service.html', {'service': service})
