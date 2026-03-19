from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import User, Patient, Provider, Scheduler
from ..serializers import UserSerializer, PatientSerializer, ProviderSerializer, SchedulerSerializer

@api_view(['GET'])
def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def get_user_by_id(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
@api_view(['GET'])
def get_all_patients(request):
    if request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_patient_by_name(request, first_name, last_name):
    try:
        patient = Patient.objects.get(first_name=first_name, last_name=last_name)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

@api_view(['GET'])
def get_all_providers(request):
    if request.method == 'GET':
        providers = Provider.objects.all()
        serializer = ProviderSerializer(providers, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_all_schedulers(request):
    if request.method == 'GET':
        schedulers = Scheduler.objects.all()
        serializer = SchedulerSerializer(schedulers, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    first_name = request.data.get("first_name")
    last_name  = request.data.get("last_name")
    phone_number = request.data.get("phone_number")
    specialty = request.data.get("specialty")

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Create the corresponding profile based on the user's role
            if user.role == 'PATIENT':
                Patient.objects.create(user_id=user, first_name=first_name, last_name=last_name, phone_number=phone_number)
            elif user.role == 'PROVIDER':
                Provider.objects.create(user_id=user, first_name=first_name, last_name=last_name,specialty=specialty)
            elif user.role == 'SCHEDULER':
                Scheduler.objects.create(user_id=user, first_name=first_name, last_name=last_name)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def update_user(request, user_id):
    first_name = request.data.get("first_name")
    last_name  = request.data.get("last_name")
    phone_number = request.data.get("phone_number")
    specialty = request.data.get("specialty")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()

            if user.role == 'PATIENT':
                patient = Patient.objects.get(user_id=user)
                patient.first_name = first_name
                patient.last_name = last_name
                patient.phone_number = phone_number
                patient.save()
            elif user.role == 'PROVIDER':
                provider = Provider.objects.get(user_id=user)
                provider.first_name = first_name
                provider.last_name = last_name
                provider.specialty = specialty
                provider.save()
            elif user.role == 'SCHEDULER':
                scheduler = Scheduler.objects.get(user_id=user)
                scheduler.first_name = first_name
                scheduler.last_name = last_name
                scheduler.save()

            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)