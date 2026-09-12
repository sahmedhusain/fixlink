import os
import sys
import random
from datetime import date, timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fixlink.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
from users.models import Customer, Company
from services.models import Service, RequestedService
from django.db.models import Avg

User = get_user_model()

def seed_database():
    print("Flushing existing database records...")
    RequestedService.objects.all().delete()
    Service.objects.all().delete()
    Company.objects.all().delete()
    Customer.objects.all().delete()
    User.objects.all().delete()

    print("Creating admin superuser...")
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@netfix.bh',
        password='adminpassword123'
    )
    print("Superuser created: username='admin', password='adminpassword123'")

    print("Creating Company accounts...")
    companies_data = [
        ('cooltech_ac', 'contact@cooltech.bh', 'Air Conditioner', 'CoolTech AC Solutions'),
        ('electro_fix', 'info@electrofix.bh', 'Electricity', 'ElectroFix Power Systems'),
        ('woodcraft_carpentry', 'sales@woodcraft.bh', 'Carpentry', 'Woodcraft Carpentry Workshop'),
        ('green_gardens', 'hello@greengardens.bh', 'Gardening', 'Green Gardens Landscaping'),
        ('prime_plumbing', 'support@primeplumbing.bh', 'Plumbing', 'Prime Plumbing & Leak Fix'),
        ('sparkle_cleaning', 'booking@sparkle.bh', 'House Keeping', 'Sparkle Home Housekeeping'),
        ('urban_interiors', 'design@urbaninteriors.bh', 'Interior Design', 'Urban Interiors BH'),
        ('allinone_services', 'info@allinone.bh', 'All in One', 'All In One Master Fix'),
        ('safe_locks', 'help@safelocks.bh', 'Locks', 'SafeLocks Emergency Locksmith'),
        ('gulf_heaters', 'service@gulfheaters.bh', 'Water Heaters', 'Gulf Water Heater Specialist'),
    ]

    companies = []
    for username, email, field, desc in companies_data:
        u = User.objects.create_user(
            username=username,
            email=email,
            password='password123',
            is_company=True
        )
        c = Company.objects.create(user=u, field=field, rating=0)
        companies.append(c)

    print("Creating Customer accounts...")
    customers_data = [
        ('sayed_h', 'sayed@example.com', date(1996, 4, 12)),
        ('ali_bahrain', 'ali.b@example.com', date(1992, 8, 25)),
        ('fatima_m', 'fatima@example.com', date(1998, 2, 14)),
        ('hassan_k', 'hassan@example.com', date(1989, 11, 30)),
        ('zainab_a', 'zainab@example.com', date(1995, 6, 18)),
        ('tariq_g', 'tariq@example.com', date(1991, 1, 5)),
        ('noor_al', 'noor@example.com', date(1999, 9, 21)),
        ('sara_v', 'sara@example.com', date(1994, 3, 10)),
    ]

    customers = []
    for username, email, birth in customers_data:
        u = User.objects.create_user(
            username=username,
            email=email,
            password='password123',
            is_customer=True
        )
        cust = Customer.objects.create(user=u, birth=birth)
        customers.append(cust)

    print("Creating Services catalog...")
    services_data = [
        # AC
        (0, 'AC Full Deep Cleaning & Washing', 'Complete indoor and outdoor coil washing, chemical cleaning, and gas check.', 18.50, 'Air Conditioner'),
        (0, 'AC Compressor Diagnostics & Fix', 'Diagnostic inspection of AC compressor, capacitor replacement, and refrigerant refill.', 25.00, 'Air Conditioner'),
        # Electricity
        (1, 'Short Circuit & Electrical Troubleshooting', 'Emergency troubleshooting for circuit breaker trips, spark outlets, and wiring faults.', 15.00, 'Electricity'),
        (1, 'Distribution Board & Breaker Upgrade', 'Complete DB panel upgrade, ELCB safety installation, and load balancing.', 32.00, 'Electricity'),
        # Carpentry
        (2, 'Custom Wooden Cabinet & Shelf Assembly', 'Professional assembly and wall mounting for custom wooden cabinets and wardrobes.', 20.00, 'Carpentry'),
        (2, 'Door Repair & Hinge Maintenance', 'Repair sticking wooden doors, frame alignment, and heavy-duty hinge fitting.', 14.00, 'Carpentry'),
        # Gardening
        (3, 'Lawn Trimming & Organic Fertilization', 'Mowing, edge trimming, weed extraction, and organic lawn fertilization service.', 12.50, 'Gardening'),
        (3, 'Irrigation Pipe Repair & Dripper Setup', 'Automatic garden drip system installation, timer programming, and leak fixes.', 22.00, 'Gardening'),
        # Plumbing
        (4, 'Main Pipe Leak Detection & Sealing', 'Ultrasound leak detection in concealed pipes and high-pressure epoxy sealing.', 28.00, 'Plumbing'),
        (4, 'Drain Unclogging & Hydro-Jet Cleaning', 'Heavy drain clearing using high-pressure hydro-jet machinery for kitchens and baths.', 16.50, 'Plumbing'),
        # House Keeping
        (5, 'Full Villa Deep Housekeeping', 'Comprehensive villa cleaning, window washing, floor scrubbing, and sanitization.', 15.00, 'House Keeping'),
        (5, 'Carpet & Sofa Steam Extraction', 'Deep stain removal and steam extraction sanitization for living room upholstery.', 18.00, 'House Keeping'),
        # Interior Design
        (6, '3D Living Room Interior Consultation', 'Full 3D layout rendering, material selection guidance, and lighting plan design.', 45.00, 'Interior Design'),
        # All in One
        (7, 'General Home Maintenance & Handyman', 'All-purpose handyman service for wall drilling, hanging, minor plumbing, and repairs.', 14.00, 'Plumbing'),
        (7, 'Complete Home Inspection & Maintenance', 'Full property structural, electrical, plumbing, and HVAC health audit.', 35.00, 'Electricity'),
        # Locks
        (8, 'Smart Digital Door Lock Installation', 'Installation and programming of biometric fingerprint and keypad smart locks.', 24.00, 'Locks'),
        # Water Heaters
        (9, 'Water Heater Element & Thermostat Replacement', 'Descaling water heater tank, heating element replacement, and thermostat calibration.', 19.00, 'Water Heaters'),
    ]

    created_services = []
    for company_idx, name, desc, price, field in services_data:
        comp = companies[company_idx]
        srv = Service.objects.create(
            company=comp,
            name=name,
            description=desc,
            price_hour=price,
            field=field
        )
        created_services.append(srv)

    print("Creating Service Requests (Bookings)...")
    addresses = [
        'Manama, Block 338, Road 3801, Villa 45',
        'Riffa, Avenue 45, Building 120, Apt 3',
        'Seef District, Tower 12, Level 8',
        'Juffair, Building 204, Road 2411',
        'Saar, Villa 88, Gate 3',
        'Amwaj Islands, Floating City, Villa 12',
        'Busaiteen, Block 224, House 19',
        'Janabiya, Avenue 27, Compound 4',
    ]

    statuses = ['Completed', 'Completed', 'Completed', 'Confirmed', 'Pending', 'Cancelled']
    now = timezone.now()

    for i in range(35):
        srv = random.choice(created_services)
        cust = random.choice(customers)
        addr = random.choice(addresses)
        hrs = random.choice([1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0])
        status = random.choice(statuses)
        cost = round(float(srv.price_hour) * hrs, 2)
        days_ago = random.randint(1, 28)
        req_date = now - timedelta(days=days_ago, hours=random.randint(1, 10))

        rating_val = None
        if status == 'Completed':
            rating_val = random.choice([4, 5, 5, 4, 3, 5])

        req = RequestedService.objects.create(
            service=srv,
            customer=cust,
            address=addr,
            hours=hrs,
            price=cost,
            status=status,
            rating=rating_val
        )
        # Update request date manually
        RequestedService.objects.filter(id=req.id).update(request_date=req_date)

    print("Recalculating Company ratings...")
    for comp in companies:
        avg_rating = RequestedService.objects.filter(
            service__company=comp,
            rating__isnull=False
        ).aggregate(Avg('rating'))['rating__avg']
        
        if avg_rating is not None:
            comp.rating = round(avg_rating)
        else:
            comp.rating = 0
        comp.save()

    print("\nSuccessfully seeded database with huge realistic dummy data!")
    print(f"Summary: {User.objects.count()} Users ({Company.objects.count()} Companies, {Customer.objects.count()} Customers), {Service.objects.count()} Services, {RequestedService.objects.count()} Requested Services.")

if __name__ == '__main__':
    seed_database()
