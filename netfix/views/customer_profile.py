from datetime import date
from django.shortcuts import render, get_object_or_404
from users.models import User, Customer
from services.models import RequestedService


def customer_profile(request, name):
    user = get_object_or_404(User, username=name)
    customer = get_object_or_404(Customer, user=user)

    birth_date = customer.birth
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    sh = RequestedService.objects.filter(customer=customer).order_by("-request_date")

    return render(request, 'users/profile.html', {
        'user': user,
        'user_age': age,
        'sh': sh
    })
