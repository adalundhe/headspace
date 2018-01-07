from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

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
    # DELETE single user
    elif request.method == 'DELETE':
        return Response({})
    # UPDATE single user
    elif request.method == 'PUT':
        return Response({})


@api_view(['GET','POST'])
def get_post_users(request):
    # GET all users
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    # POST new user
    elif request.method == 'POST':
        return Response({})
