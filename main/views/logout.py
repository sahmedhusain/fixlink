from django.shortcuts import render
from django.contrib.auth import logout as django_logout


def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")
