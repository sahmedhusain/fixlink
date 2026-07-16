from django.shortcuts import render, get_object_or_404
from users.models import User, Company
from services.models import Service


from django.http import Http404

def company_profile(request, name):
    user = get_object_or_404(User, username=name)
    try:
        company = Company.objects.get(user=user)
    except Company.DoesNotExist:
        if user.is_superuser:
            company, _ = Company.objects.get_or_create(user=user, defaults={'field': 'All in One'})
        else:
            raise Http404("Company profile not found")
            
    services = Service.objects.filter(company=company).order_by("-date")


    return render(request, 'users/profile.html', {
        'user': user,
        'services': services
    })
