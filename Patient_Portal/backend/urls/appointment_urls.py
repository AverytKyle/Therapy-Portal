from django.urls import path
from ..views.appointment_views import *

urlpatterns = [
    path('', get_all_appointments, name='get_all_appointments'),
    path('<int:appointment_id>/', get_appointment_by_id, name='get_appointment_by_id'),
    path('create/', create_appointment, name='create_appointment'),
    path('update/<int:appointment_id>/', update_appointment, name='update_appointment'),
    path('delete/<int:appointment_id>/', delete_appointment, name='delete_appointment'),
]