from django.shortcuts import render, get_object_or_404
from users.models import User, Company
from services.models import Service


def company_profile(request, name):
    user = get_object_or_404(User, username=name)
    company = get_object_or_404(Company, user=user)
    services = Service.objects.filter(company=company).order_by("-date")

    return render(request, 'users/profile.html', {
        'user': user,
        'services': services
    })
