from datetime import date
from django.shortcuts import render
from django.db.models import Sum
from collections import defaultdict
from users.models import Company, Customer
from services.models import Service, RequestedService


def home(request):
    if request.user.is_authenticated:
        if request.user.is_customer:
            # Load Customer Dashboard
            try:
                customer = Customer.objects.get(user=request.user)
            except Customer.DoesNotExist:
                if request.user.is_superuser:
                    customer, _ = Customer.objects.get_or_create(user=request.user, defaults={'birth': date(2000, 1, 1)})
                else:
                    return render(request, "main/home.html", {'is_guest': True})

            birth_date = customer.birth
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

            sh = RequestedService.objects.filter(customer=customer).order_by("-request_date")
            total_spent = sh.exclude(status='Cancelled').aggregate(Sum('price'))['price__sum'] or 0.00
            bookings_count = sh.count()
            completed_count = sh.filter(status='Completed').count()
            pending_count = sh.filter(status='Pending').count()

            return render(request, "main/home.html", {
                'is_customer': True,
                'customer': customer,
                'user_age': age,
                'sh': sh,
                'total_spent': total_spent,
                'bookings_count': bookings_count,
                'completed_count': completed_count,
                'pending_count': pending_count
            })

        elif request.user.is_company or request.user.is_superuser:
            # Load Company Dashboard
            try:
                company = Company.objects.get(user=request.user)
            except Company.DoesNotExist:
                if request.user.is_superuser:
                    company, _ = Company.objects.get_or_create(user=request.user, defaults={'field': 'All in One'})
                else:
                    return render(request, "main/home.html", {'is_guest': True})

            services = Service.objects.filter(company=company).order_by("-date")
            incoming_bookings = RequestedService.objects.filter(service__company=company).order_by("-request_date")

            total_revenue = incoming_bookings.filter(status='Completed').aggregate(Sum('price'))['price__sum'] or 0.00
            completed_jobs = incoming_bookings.filter(status='Completed').count()
            active_jobs = incoming_bookings.filter(status='Confirmed').count()
            pending_approvals = incoming_bookings.filter(status='Pending').count()

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

            return render(request, "main/home.html", {
                'is_company': True,
                'company': company,
                'services': services,
                'incoming_bookings': incoming_bookings,
                'total_revenue': total_revenue,
                'completed_jobs': completed_jobs,
                'active_jobs': active_jobs,
                'pending_approvals': pending_approvals,
                'crm_customers': crm_customers
            })

    # Guest user: show service dashboard (all services list)
    services = Service.objects.all().order_by("-date")
    return render(request, "main/home.html", {
        'is_guest': True,
        'services': services
    })
