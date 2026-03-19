from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import TreatmentType
from ..serializers import TreatmentTypeSerializer

@api_view(['GET'])
def get_all_treatment_types(request):
    if request.method == 'GET':
        treatment_types = TreatmentType.objects.all()
        serializer = TreatmentTypeSerializer(treatment_types, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def get_treatment_type_by_id(request, treatment_type_id):
    try:
        treatment_type = TreatmentType.objects.get(id=treatment_type_id)
    except TreatmentType.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TreatmentTypeSerializer(treatment_type)
        return Response(serializer.data)
    
@api_view(['POST'])
def create_treatment_type(request):
    serializer = TreatmentTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_treatment_type(request, treatment_type_id):
    try:
        treatment_type = TreatmentType.objects.get(id=treatment_type_id)
    except TreatmentType.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    treatment_type.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)