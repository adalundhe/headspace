from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Incident
from .serializers import IncidentSerializer
from datetime import datetime

# Create your views here.

@api_view(['GET','DELETE','PUT'])
def get_delete_update_incident(request, pk):
    try:
        incident = Incident.objects.get(pk=pk)
    except Incident.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    # GET single incident
    if request.method == 'GET':
        serializer = IncidentSerializer(incident)
        return Response(serializer.data)


    # UPDATE single incident
    elif request.method == 'PUT':
        try:
            data = {
                'description': request.data.get('description'),
                'painlevel': request.data.get('painlevel'),
                'headaches': request.data.get('headaches'),
                'fainting': request.data.get('fainting'),
                'speechloss': request.data.get('speechloss'),
                'occurence': datetime.strptime(request.data.get('occurence'),'%b %d %Y %I:%M%p'),
                'duration': request.data.get('duration'),
                'userid': request.data.get('userid')
            }
            serializer = IncidentSerializer(incident, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response('Failed to insert: Missing Value.', status=status.HTTP_400_BAD_REQUEST)


    # DELETE single user
    elif request.method == 'DELETE':
        incident.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def get_post_incidents(request):
    # GET all incidents
    if request.method == 'GET':
        incidents = Incident.objects.all()
        serializer = IncidentSerializer(incidents, many=True)
        return Response(serializer.data)


    # POST new incident
    elif request.method == 'POST':
        try:
            data = {
                'description': request.data.get('description'),
                'painlevel': request.data.get('painlevel'),
                'headaches': request.data.get('headaches'),
                'fainting': request.data.get('fainting'),
                'speechloss': request.data.get('speechloss'),
                'occurence': datetime.strptime(request.data.get('occurence'),'%b %d %Y %I:%M%p'),
                'duration': request.data.get('duration'),
                'userid': request.data.get('userid')
            }
            serializer = IncidentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response('Failed to insert: Missing Value.', status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_incidents_by_user(request, userid):
    # Get incidents by userid
    try:
        incidents = Incident.objects.filter(userid=userid)
    except Incident.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    # GET incidents matching userid
    if request.method == 'GET':
        serializer = IncidentSerializer(incidents, many=True)
        if len(serializer.data) > 0:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
