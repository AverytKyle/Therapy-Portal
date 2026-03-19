from django.urls import path, include

urlpatterns = [
    path('users/', include('backend.urls.user_urls')),
    path('appointments/', include('backend.urls.appointment_urls')),
    path('treatment_types/', include('backend.urls.treatmentType_urls')),
]