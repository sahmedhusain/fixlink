from django.shortcuts import render
from django.db.models import Count
from services.models import Service


def most_requested(request):
    services = Service.objects.annotate(request_count=Count('requestedservice')).order_by('-request_count')
    return render(request, 'services/most_requested.html', {'services': services})
