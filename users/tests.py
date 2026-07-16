from datetime import date
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from users.models import Customer, Company
from services.models import Service, RequestedService
from users.forms import CustomerSignUpForm, CompanySignUpForm, validate_email

User = get_user_model()


class NetfixTestCase(TestCase):
    def setUp(self):
        # Create an All in One company
        self.company_user1 = User.objects.create_user(
            username='allinone_co',
            email='allinone@example.com',
            password='password123',
            is_company=True
        )
        self.company1 = Company.objects.create(
            user=self.company_user1,
            field='All in One'
        )

        # Create an Electricity company
        self.company_user2 = User.objects.create_user(
            username='electric_co',
            email='electric@example.com',
            password='password123',
            is_company=True
        )
        self.company2 = Company.objects.create(
            user=self.company_user2,
            field='Electricity'
        )

        # Create a Customer
        self.customer_user = User.objects.create_user(
            username='john_doe',
            email='john@example.com',
            password='password123',
            is_customer=True
        )
        self.customer = Customer.objects.create(
            user=self.customer_user,
            birth=date(1995, 5, 15)
        )

    def test_email_uniqueness_validation(self):
        # Test unique email validator
        with self.assertRaises(ValidationError):
            validate_email('john@example.com')

    def test_customer_creation(self):
        self.assertEqual(self.customer.user.username, 'john_doe')
        self.assertEqual(self.customer.birth, date(1995, 5, 15))

    def test_company_field_restrictions(self):
        # All in One company can create any services
        service1 = Service.objects.create(
            company=self.company1,
            name='AC Fix',
            description='Fixing AC',
            price_hour=15.00,
            field='Air Conditioner'
        )
        self.assertEqual(service1.field, 'Air Conditioner')

        # Electricity company can create Electricity services
        service2 = Service.objects.create(
            company=self.company2,
            name='Wire Change',
            description='Change house wiring',
            price_hour=20.00,
            field='Electricity'
        )
        self.assertEqual(service2.field, 'Electricity')

    def test_service_request_cost_calculation(self):
        service = Service.objects.create(
            company=self.company2,
            name='Wire Change',
            description='Change house wiring',
            price_hour=10.50,
            field='Electricity'
        )

        # Request service for 2 hours
        req = RequestedService.objects.create(
            service=service,
            customer=self.customer,
            address='123 Main St',
            hours=2.00,
            price=2.00 * float(service.price_hour)
        )

        self.assertEqual(req.price, 21.00)
        self.assertEqual(RequestedService.objects.filter(customer=self.customer).count(), 1)

    def test_most_requested_services(self):
        service_ac = Service.objects.create(
            company=self.company1,
            name='AC Service',
            description='AC Repair',
            price_hour=10.00,
            field='Air Conditioner'
        )
        service_plumb = Service.objects.create(
            company=self.company1,
            name='Plumbing Service',
            description='Pipe Repair',
            price_hour=12.00,
            field='Plumbing'
        )

        # Request AC service once
        RequestedService.objects.create(
            service=service_ac,
            customer=self.customer,
            address='Address 1',
            hours=1,
            price=10.00
        )

        # Request Plumbing service twice
        RequestedService.objects.create(
            service=service_plumb,
            customer=self.customer,
            address='Address 1',
            hours=1,
            price=12.00
        )
        RequestedService.objects.create(
            service=service_plumb,
            customer=self.customer,
            address='Address 2',
            hours=2,
            price=24.00
        )

        # Check most requested query
        from django.db.models import Count
        most_requested = Service.objects.annotate(
            request_count=Count('requestedservice')
        ).order_by('-request_count')

        self.assertEqual(most_requested[0], service_plumb)
        self.assertEqual(most_requested[0].request_count, 2)
        self.assertEqual(most_requested[1], service_ac)
        self.assertEqual(most_requested[1].request_count, 1)

    def test_booking_status_workflow(self):
        service = Service.objects.create(
            company=self.company2,
            name='Wire Change',
            description='Description',
            price_hour=10.00,
            field='Electricity'
        )
        booking = RequestedService.objects.create(
            service=service,
            customer=self.customer,
            address='123 Main St',
            hours=2.00,
            price=20.00
        )
        self.assertEqual(booking.status, 'Pending')

        # Test company confirmation
        self.client.force_login(self.company_user2)
        response = self.client.post(f'/services/booking/{booking.id}/confirm/')
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'Confirmed')

        # Test company completion
        response = self.client.post(f'/services/booking/{booking.id}/complete/')
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'Completed')

    def test_booking_cancellation(self):
        service = Service.objects.create(
            company=self.company2,
            name='Wire Change',
            description='Description',
            price_hour=10.00,
            field='Electricity'
        )
        booking = RequestedService.objects.create(
            service=service,
            customer=self.customer,
            address='123 Main St',
            hours=2.00,
            price=20.00
        )

        # Test customer cancellation of pending booking
        self.client.force_login(self.customer_user)
        response = self.client.post(f'/services/booking/{booking.id}/cancel/')
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'Cancelled')

    def test_booking_rating_recalculation(self):
        service = Service.objects.create(
            company=self.company2,
            name='Wire Change',
            description='Description',
            price_hour=10.00,
            field='Electricity'
        )
        booking1 = RequestedService.objects.create(
            service=service,
            customer=self.customer,
            address='Address',
            hours=2.00,
            price=20.00,
            status='Completed'
        )
        booking2 = RequestedService.objects.create(
            service=service,
            customer=self.customer,
            address='Address',
            hours=3.00,
            price=30.00,
            status='Completed'
        )

        # Log in customer to rate them
        self.client.force_login(self.customer_user)

        # Rate booking1 with 4
        self.client.post(f'/services/booking/{booking1.id}/rate/', {'rating': 4})
        self.company2.refresh_from_db()
        self.assertEqual(self.company2.rating, 4)

        # Rate booking2 with 2
        self.client.post(f'/services/booking/{booking2.id}/rate/', {'rating': 2})
        self.company2.refresh_from_db()
        # Average is (4 + 2) / 2 = 3
        self.assertEqual(self.company2.rating, 3)

