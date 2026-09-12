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

    from services.models import RequestedService
    incoming_bookings = RequestedService.objects.filter(service__company=company).order_by("-request_date")

    from django.db.models import Sum
    total_revenue = incoming_bookings.filter(status='Completed').aggregate(Sum('price'))['price__sum'] or 0.00
    completed_jobs = incoming_bookings.filter(status='Completed').count()
    active_jobs = incoming_bookings.filter(status='Confirmed').count()
    pending_approvals = incoming_bookings.filter(status='Pending').count()

    from collections import defaultdict
    customer_stats = defaultdict(lambda: {'spent': 0.00, 'bookings': 0, 'username': '', 'email': ''})
    for booking in incoming_bookings:
        cust = booking.customer
        c_username = cust.user.username
        customer_stats[c_username]['username'] = c_username
        customer_stats[c_username]['email'] = cust.user.email
        customer_stats[c_username]['bookings'] += 1
        if booking.status == 'Completed':
            customer_stats[c_username]['spent'] += float(booking.price)

    crm_customers = sorted(customer_stats.values(), key=lambda x: x['spent'], reverse=True)

    return render(request, 'users/profile.html', {
        'user': user,
        'services': services,
        'incoming_bookings': incoming_bookings,
        'total_revenue': total_revenue,
        'completed_jobs': completed_jobs,
        'active_jobs': active_jobs,
        'pending_approvals': pending_approvals,
        'crm_customers': crm_customers
    })

