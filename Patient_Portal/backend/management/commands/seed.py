from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from faker import Faker
import random
from datetime import timedelta, time

from backend.models import (
    User,
    Patient,
    Provider,
    Scheduler,
    TreatmentType,
    Appointment
)
fake = Faker()


class Command(BaseCommand):
    help = "Seed the entire database with initial data"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Seeding database..."))

        self.seed_treatments()
        schedulers = self.seed_schedulers()
        providers = self.seed_providers()
        patients = self.seed_patients()
        self.seed_appointments(providers, patients)

        self.stdout.write(self.style.SUCCESS("Seeding complete!"))

    # -------------------------
    # TREATMENTS
    # -------------------------
    def seed_treatments(self):
        treatments = [
            ("Chiro", 10),
            ("MCU", 30),
            ("Physio", 30),
            ("Laser", 10),
            ("Traction", 30),
        ]

        for name, duration in treatments:
            TreatmentType.objects.get_or_create(
                name=name,
                defaults={"duration_minutes": duration}
            )

        self.stdout.write(self.style.SUCCESS("Treatment types seeded"))

    # -------------------------
    # SCHEDULER USER
    # -------------------------
    def seed_schedulers(self):
        schedulers = []

        for i in range(2):
            username = f"scheduler{i}"

            if not User.objects.filter(username=username).exists():
                user = User.objects.create(
                    username=username,
                    email=f"{username}@clinic.com",
                    password=make_password("password123"),
                    pin=123456,
                    role="SCHEDULER",
                )

                scheduler = Scheduler.objects.create(
                    user_id=user,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                )

                schedulers.append(scheduler)

        self.stdout.write(self.style.SUCCESS("Schedulers seeded"))
        return Scheduler.objects.all()

    # -------------------------
    # PROVIDERS
    # -------------------------
    def seed_providers(self):
        providers = []

        for i in range(3):
            username = f"provider{i}"

            if not User.objects.filter(username=username).exists():
                user = User.objects.create(
                    username=username,
                    email=f"{username}@clinic.com",
                    password=make_password("password123"),
                    pin=123456,
                    role="PROVIDER",
                )

                provider = Provider.objects.create(
                    user_id=user,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    specialty="Chiropractor",
                )

                providers.append(provider)

        self.stdout.write(self.style.SUCCESS("Providers seeded"))
        return Provider.objects.all()

    # -------------------------
    # PATIENTS
    # -------------------------
    def seed_patients(self):
        patients = []

        for i in range(20):
            username = f"patient{i}"

            if not User.objects.filter(username=username).exists():
                user = User.objects.create(
                    username=username,
                    email=f"{username}@clinic.com",
                    password=make_password("password123"),
                    pin=123456,
                    role="PATIENT",
                )

                patient = Patient.objects.create(
                    user_id=user,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    phone_number=fake.phone_number(),
                )

                patients.append(patient)

        self.stdout.write(self.style.SUCCESS("Patients seeded"))
        return Patient.objects.all()

    # -------------------------
    # APPOINTMENTS
    # -------------------------
    def seed_appointments(self, providers, patients):
        treatments = list(TreatmentType.objects.all())
        today = timezone.now().date()

        for _ in range(40):
            provider = random.choice(providers)
            patient = random.choice(patients)
            treatment = random.choice(treatments)

            start_hour = random.randint(8, 16)
            start_time = time(start_hour, 0)
            end_time = (timezone.datetime.combine(today, start_time)
                        + timedelta(minutes=30)).time()

            scheduler = Scheduler.objects.first()

            appointment = Appointment.objects.create(
                patient=patient,
                provider=provider,
                treatment_type=treatment,
                date=today + timedelta(days=random.randint(0, 5)),
                start_time=start_time,
                end_time=end_time,
                status="SCHEDULED",
                created_by=scheduler
            )

        self.stdout.write(self.style.SUCCESS("Appointments seeded"))