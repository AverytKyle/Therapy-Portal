from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('PROVIDER', 'Provider'),
        ('SCHEDULER', 'Scheduler'),
    )

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    pin = models.IntegerField(max_length=6)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_patient(self):
        return self.role == 'PATIENT'
    
    def is_provider(self):
        return self.role == 'PROVIDER'
    
    def is_scheduler(self):
        return self.role == 'SCHEDULER'
    
    def __str__(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
        }
    
class Provider(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)

    def __str__(self):
        return {
            'id': self.user_id.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'specialty': self.specialty,
        }
    
class Patient(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return {
            'id': self.user_id.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
        }
    
class Scheduler(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return {
            'id': self.user_id.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
    
class TreatmentType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    duration_minutes = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return {
            'id': self.id,
            'name': self.name,
            'duration_minutes': self.duration_minutes,
            'description': self.description,
        }
    
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled'),
    )

    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    treatment_type = models.ForeignKey(TreatmentType, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(Scheduler, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'start_time']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['provider', 'date']),
            models.Index(fields=['patient', 'date']),
        ]

    def __str__(self):
        return {
            'id': self.id,
            'patient_id': self.patient.user_id.id,
            'provider_id': self.provider.user_id.id,
            'treatment_type_id': self.treatment_type.id,
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'status': self.status,
        }