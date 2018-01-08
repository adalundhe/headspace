from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Symptom
from .serializers import SymptomSerializer

# Create your views here.
@api_view(['get','DELETE','PUT'])
def get_delete_update_symptom(request, pk):
    try:
        symptom = Symptom.objects.get(pk=pk)
    except Symptom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    # GET single symptom
    if request.method == 'GET':
        serializer = SymptomSerializer(symptom)
        return Response(serializer.data)


    # UPDATE single symptom
    elif request.method == 'PUT':
        try:
            data = {
                'incidentid': request.data.get('incidentid'),
                'userid': request.data.get('userid'),
                'type_of': request.data.get('type_of'),
                'description': request.data.get('description'),
                'commonality': request.data.get('commonality'),
                'name': request.data.get('name'),
                'location': request.data.get('location')
            }
            serializer = SymptomSerializer(symptom, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response('Failed to insert: Missing value.', status=status.HTTP_400_BAD_REQUEST)

    # DELETE single user
    elif request.method == 'DELETE':
        symptom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def get_post_symptoms(request):
    # GET all symptoms
    if request.method == 'GET':
        symptoms = Symptom.objects.all()
        serializer = SymptomSerializer(symptoms, many=True)
        return Response(serializer.data)

    # POST new symptom
    elif request.method == 'POST':
        try:
            data = {
                'incidentid': request.data.get('incidentid'),
                'userid': request.data.get('userid'),
                'type_of': request.data.get('type_of'),
                'description': request.data.get('description'),
                'commonality': request.data.get('commonality'),
                'name': request.data.get('name'),
                'location': request.data.get('location')
            }
            serializer = SymptomSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response('Failed to insert: Missing value.', status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_symptoms_by_user_and_incident(request, userid, incidentid=None):
    # Get symptom by userid and incidentid
    try:
        symptoms = Symptom.objects.filter(userid=userid, incidentid=incidentid)
    except Symptom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET symptoms matching userid and incidentid
    if request.method == 'GET':
        serializer = SymptomSerializer(symptoms, many=True)
        if len(serializer.data) > 0:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_symptoms_by_user(request, userid):
    # Get symptoms by userid
    try:
        symptoms = Symptom.objects.filter(userid=userid)
    except Symptom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET symptoms matching userid
    if request.method == 'GET':
        serializer = SymptomSerializer(symptoms, many=True)
        if len(serializer.data) > 0:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
