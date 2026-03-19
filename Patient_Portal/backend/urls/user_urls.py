from django.urls import path
from ..views.user_views import *
from ..views.session_views import restore_user

urlpatterns = [
    path('', get_all_users, name='get_all_users'),
    path('<int:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('patients/', get_all_patients, name='get_all_patients'),
    path('session/', restore_user, name='restore_user'),
    path('patients/<str:first_name>/<str:last_name>/', get_patient_by_name, name='get_patient_by_name'),
    path('providers/', get_all_providers, name='get_all_providers'),
    path('schedulers/', get_all_schedulers, name='get_all_schedulers'),
    path('create/', create_user, name='create_user'),
    path('update/<int:user_id>/', update_user, name='update_user'),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),
]