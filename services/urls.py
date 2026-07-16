from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.service_list, name='services_list'),
    path('create/', v.create, name='services_create'),
    path('<int:id>', v.index, name='index'),
    path('<int:id>/request_service/', v.request_service, name='request_service'),
    path('most_requested/', v.most_requested, name='most_requested'),
    path('booking/<int:booking_id>/confirm/', v.confirm_booking, name='confirm_booking'),
    path('booking/<int:booking_id>/complete/', v.complete_booking, name='complete_booking'),
    path('booking/<int:booking_id>/cancel/', v.cancel_booking, name='cancel_booking'),
    path('booking/<int:booking_id>/rate/', v.rate_booking, name='rate_booking'),
    path('<slug:field>/', v.service_field, name='services_field'),


]
