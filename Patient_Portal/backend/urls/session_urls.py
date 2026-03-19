from django.urls import path
from ..views.session_views import restore_user

urlpatterns = [
    path('', restore_user, name='session'),
]
