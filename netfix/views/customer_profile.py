from datetime import date
from django.shortcuts import render, get_object_or_404
from users.models import User, Customer
from services.models import RequestedService


from django.http import Http404

def customer_profile(request, name):
    user = get_object_or_404(User, username=name)
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        if user.is_superuser:
            customer, _ = Customer.objects.get_or_create(user=user, defaults={'birth': date(2000, 1, 1)})
        else:
            raise Http404("Customer profile not found")

    birth_date = customer.birth

    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    sh = RequestedService.objects.filter(customer=customer).order_by("-request_date")

    return render(request, 'users/profile.html', {
        'user': user,
        'user_age': age,
        'sh': sh
    })
