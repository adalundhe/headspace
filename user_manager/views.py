from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from datetime import datetime

@api_view(['GET','DELETE','PUT'])
def get_delete_update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    # GET single user
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # UPDATE single user
    elif request.method == 'PUT':
        try:
            data = {
                'firstname': request.data.get('firstname'),
                'lastname': request.data.get('lastname'),
                'injury': request.data.get('injury'),
                'incidents': request.data.get('incidents'),
                'incidentdate': datetime.strptime(request.data.get('incidentdate'),'%b %d %Y %I:%M%p'),
                'recoverydate': datetime.strptime(request.data.get('recoverydate'),'%b %d %Y %I:%M%p')
            }
            serializer = UserSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response('Failed to insert: Missing value.', status=status.HTTP_400_BAD_REQUEST)

    # DELETE single user
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def get_post_users(request):
    # GET all users
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    # POST new user
    elif request.method == 'POST':
        try:
            data = {
                'firstname': request.data.get('firstname'),
                'lastname': request.data.get('lastname'),
                'injury': request.data.get('injury'),
                'incidents': request.data.get('incidents'),
                'incidentdate': datetime.strptime(request.data.get('incidentdate'),'%b %d %Y %I:%M%p'),
                'recoverydate': datetime.strptime(request.data.get('recoverydate'),'%b %d %Y %I:%M%p')
            }
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response('Failed to insert: Missing value.', status=status.HTTP_400_BAD_REQUEST)
