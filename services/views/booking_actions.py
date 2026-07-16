from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.db.models import Avg
from services.models import RequestedService
from users.models import Company, Customer


@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(RequestedService, id=booking_id)
    if not getattr(request.user, 'is_company', False):
        return HttpResponseForbidden("Only companies can confirm bookings.")

    company = get_object_or_404(Company, user=request.user)
    if booking.service.company != company:
        return HttpResponseForbidden("You can only manage bookings for your own services.")

    if booking.status == 'Pending':
        booking.status = 'Confirmed'
        booking.save()

    return redirect('/company/' + request.user.username)


@login_required
def complete_booking(request, booking_id):
    booking = get_object_or_404(RequestedService, id=booking_id)
    if not getattr(request.user, 'is_company', False):
        return HttpResponseForbidden("Only companies can complete bookings.")

    company = get_object_or_404(Company, user=request.user)
    if booking.service.company != company:
        return HttpResponseForbidden("You can only manage bookings for your own services.")

    if booking.status == 'Confirmed':
        booking.status = 'Completed'
        booking.save()

    return redirect('/company/' + request.user.username)


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(RequestedService, id=booking_id)
    
    # Allowed if user is the customer who made it or the company providing the service
    is_owner = False
    if getattr(request.user, 'is_customer', False):
        customer = get_object_or_404(Customer, user=request.user)
        if booking.customer == customer:
            is_owner = True
            
    if getattr(request.user, 'is_company', False):
        company = get_object_or_404(Company, user=request.user)
        if booking.service.company == company:
            is_owner = True

    if not is_owner:
        return HttpResponseForbidden("You are not authorized to cancel this booking.")

    if booking.status in ['Pending', 'Confirmed']:
        booking.status = 'Cancelled'
        booking.save()

    if getattr(request.user, 'is_customer', False):
        return redirect('/customer/' + request.user.username)
    else:
        return redirect('/company/' + request.user.username)


@login_required
def rate_booking(request, booking_id):
    booking = get_object_or_404(RequestedService, id=booking_id)
    if not getattr(request.user, 'is_customer', False):
        return HttpResponseForbidden("Only customers can rate bookings.")

    customer = get_object_or_404(Customer, user=request.user)
    if booking.customer != customer:
        return HttpResponseForbidden("You can only rate your own requested services.")

    if booking.status != 'Completed':
        return HttpResponseBadRequest("You can only rate completed services.")

    if request.method == 'POST':
        try:
            rating_val = int(request.POST.get('rating', 0))
            if rating_val < 1 or rating_val > 5:
                return HttpResponseBadRequest("Rating must be between 1 and 5.")
            
            booking.rating = rating_val
            booking.save()

            # Recalculate average rating of the Company
            company = booking.service.company
            avg_rating = RequestedService.objects.filter(
                service__company=company, 
                rating__isnull=False
            ).aggregate(Avg('rating'))['rating__avg']

            if avg_rating is not None:
                company.rating = round(avg_rating)
                company.save()
        except ValueError:
            return HttpResponseBadRequest("Invalid rating value.")

    return redirect('/customer/' + request.user.username)
