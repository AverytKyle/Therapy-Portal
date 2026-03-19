from django.urls import path
from ..views.treatmentType_views import *

urlpatterns = [
    path('', get_all_treatment_types, name='get_all_treatment_types'),
    path('<int:treatment_type_id>/', get_treatment_type_by_id, name='get_treatment_type_by_id'),
    path('create/', create_treatment_type, name='create_treatment_type'),
    path('delete/<int:treatment_type_id>/', delete_treatment_type, name='delete_treatment_type'),
]