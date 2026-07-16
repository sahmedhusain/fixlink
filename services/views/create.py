from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from services.forms import CreateNewService
from services.models import Service
from users.models import Company


@login_required
def create(request):
    if not getattr(request.user, 'is_company', False):
        return redirect('/')

    company = Company.objects.get(user=request.user)

    if company.field == 'All in One':
        choices = Service.choices
    else:
        choices = [(company.field, company.field)]

    if request.method == 'POST':
        form = CreateNewService(request.POST, choices=choices)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            price_hour = form.cleaned_data.get('price_hour')
            field = form.cleaned_data.get('field')

            if company.field != 'All in One' and field != company.field:
                form.add_error('field', "You are not allowed to create a service in this field.")
            else:
                Service.objects.create(
                    company=company,
                    name=name,
                    description=description,
                    price_hour=price_hour,
                    field=field
                )
                return redirect('/company/' + request.user.username)
    else:
        form = CreateNewService(choices=choices)

    return render(request, 'services/create.html', {'form': form})
