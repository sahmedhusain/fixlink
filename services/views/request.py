from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from services.models import Service, RequestedService
from services.forms import RequestServiceForm
from users.models import Customer


@login_required
def request_service(request, id):
    if not getattr(request.user, 'is_customer', False):
        return redirect('/')

    service = get_object_or_404(Service, id=id)
    customer = get_object_or_404(Customer, user=request.user)

    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data.get('address')
            hours = form.cleaned_data.get('hours')
            price = hours * service.price_hour

            RequestedService.objects.create(
                service=service,
                customer=customer,
                address=address,
                hours=hours,
                price=price
            )
            return redirect('/customer/' + request.user.username)
    else:
        form = RequestServiceForm()

    return render(request, 'services/request_service.html', {'form': form, 'service': service})
